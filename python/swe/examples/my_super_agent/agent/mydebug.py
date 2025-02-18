import json
from collections import defaultdict
from pprint import pprint as pp
from langgraph.prebuilt import ToolNode

from inputs import from_github
from langchain_core.messages import HumanMessage
import traceback
from composio import Action
import uuid 
from pathlib import Path

from agent import get_agent_graph
from tools import create_pr


def main() -> None:
    """Run the agent."""
    repo, issue = "23jura23/python-example-project", ""
    # repo, issue = "a/b", ""
    owner, repo_name = repo.split("/")

    repo_path = f"<path to cloned project>"

    graph, composio_toolset, run_file = get_agent_graph(
        repo_path=repo_path,
        workspace_id=""
    )
    composio_toolset.execute_action(
        action=Action.FILETOOL_GIT_CLONE,
        params={
            "repo_name": f"{owner}/{repo_name}"
        },
    )
    composio_toolset.execute_action(
        action=Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
        params={"path": str(repo_path)},
    )
    composio_toolset.execute_action(
        action=Action.CODE_ANALYSIS_TOOL_CREATE_CODE_MAP,
        params={},
    )

    tools_inputs_outputs = {
        Action.FILETOOL_GIT_REPO_TREE: {
            "input": {
                "git_repo_path": repo_path
            },
        },
        Action.FILETOOL_LIST_FILES: {
            "input": {},
        },
        Action.FILETOOL_OPEN_FILE: {
            "input": {
                "file_path": "calculator_app.py",
                "line_number": 5
            },
        },
        Action.FILETOOL_SCROLL: {
            "input": {
                "direction": "down",
                "lines": 10
            },
        },
        Action.FILETOOL_EDIT_FILE: {
            "input": {
                "file_path": "calculator_app.py",
                "text": "# super cool comment!",
                "start_line": 20,
                "end_line": 20
            },
        },
        Action.FILETOOL_CREATE_FILE: {
            "input": {
                "path": "new_file.py",
                "is_directory": False,
            },
        },
        Action.FILETOOL_FIND_FILE: {
            "input": {
                "pattern": ".*py",
                "depth": 1,
                "case_sensitive": False,
                "include": [],
                "exclude": [],
            },
        },
        Action.FILETOOL_SEARCH_WORD: {
            "input": {
                "word": "calc",
                "pattern": "*.py",
                "recursive": True,
                "case_insensitive": True,
                "exclude": [],
            },
        },
        Action.FILETOOL_WRITE: {
            "input": {
                "file_path": "new_file.py",
                "text": "print('Super text!')",
            },
        },
        Action.FILETOOL_GIT_PATCH: {
            "input": {
                "new_file_paths": ["new_file.py", ],
            },
        },
        Action.CODE_ANALYSIS_TOOL_GET_CLASS_INFO: {
            "input": {
                "class_name": "Calculator",
            },
        },
        Action.CODE_ANALYSIS_TOOL_GET_METHOD_BODY: {
            "input": {
                "class_name": "Calculator",
                "method_name": "add",
            },
        },
        Action.CODE_ANALYSIS_TOOL_GET_METHOD_SIGNATURE: {
            "input": {
                "class_name": "Calculator",
                "method_name": "add",
            },
        },
    }

    def field_info_to_dict(finfo):
        d = {}
        d["required"] = finfo.is_required()
        if not finfo.is_required():
            d["default"] = finfo.default
        d["description"] = finfo.description
        d["annotation"] = str(finfo.annotation)
        return d

    def get_tool_inputs_outputs(action):
        from composio.tools.local import (  # pylint: disable=import-outside-toplevel
            load_local_tools,
        )


        action = Action(action)
        registry = load_local_tools()
        tool = (
            registry["runtime"][action.app]
            if action.is_runtime
            else registry["local"][action.app]
        )
        input_model = {k: field_info_to_dict(v) for k, v in tool._actions.get(action).request.model.model_fields.items()}
        output_model = {k: field_info_to_dict(v) for k, v in tool._actions.get(action).response.model.model_fields.items()}
        exclude = ["file_manager_id", "scroll_id"]
        for ex in exclude:
            if ex in input_model:
                del input_model[ex]
        return input_model, output_model

    res = []
    for tool_name, tool_args in tools_inputs_outputs.items():
        d = defaultdict(dict)
        tool_input = tool_args["input"]
        io_model = get_tool_inputs_outputs(tool_name)
        d["name"] = tool_name.name
        d["input"]["example"] = tool_input
        d["input"]["model"] = io_model[0]
        try:
            tool_output = composio_toolset.execute_action(
                action=tool_name,
                params=tool_input,
            )
            d["output"]["example"] = tool_output["data"]
            d["output"]["model"] = io_model[1]
        except Exception as e:
            print("Error raised while agent execution: \n", traceback.format_exc())
        res.append(d)
    with open("tools_outputs_examples.json", "w") as f:
        json.dump(res, f, indent=2, sort_keys=True)

# swe_tools = [
    #         *composio_toolset.get_tools(
    #             actions=[
    #                 Action.FILETOOL_OPEN_FILE,
    #                 Action.FILETOOL_GIT_REPO_TREE,
    #                 Action.FILETOOL_GIT_PATCH,
    #             ]
    #         ),
    #     ]
    # # Separate tools into two groups
    # code_analysis_tools = [
    #     *composio_toolset.get_tools(
    #         actions=[
    #             Action.CODE_ANALYSIS_TOOL_GET_CLASS_INFO,
    #             Action.CODE_ANALYSIS_TOOL_GET_METHOD_BODY,
    #             Action.CODE_ANALYSIS_TOOL_GET_METHOD_SIGNATURE,
    #             # Action.CODE_ANALYSIS_TOOL_GET_RELEVANT_CODE
    #         ]
    #     ),
    # ]
    # file_tools = [
    #     *composio_toolset.get_tools(
    #         actions=[
    #             Action.FILETOOL_GIT_REPO_TREE,
    #             Action.FILETOOL_LIST_FILES,
    #             Action.FILETOOL_CHANGE_WORKING_DIRECTORY,
    #             Action.FILETOOL_OPEN_FILE,
    #             Action.FILETOOL_SCROLL,
    #             Action.FILETOOL_EDIT_FILE,
    #             Action.FILETOOL_CREATE_FILE,
    #             Action.FILETOOL_FIND_FILE,
    #             Action.FILETOOL_SEARCH_WORD,
    #             Action.FILETOOL_WRITE,
    #         ]
    #     ),
    # ]
    #
    # code_analysis_tool_node = ToolNode(code_analysis_tools)
    # file_tool_node = ToolNode(file_tools)
    # swe_tool_node = ToolNode(swe_tools)
    #
    # swe_tools[0]
    # code_analysis_tool_node.

    

if __name__ == "__main__":
    main()
