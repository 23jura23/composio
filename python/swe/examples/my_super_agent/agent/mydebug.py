import json

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
    repo, issue = "23jura23/munich-scripts", "Script stopped working, can you fix it?"
    # repo, issue = "a/b", ""
    owner, repo_name = repo.split("/")

    repo_path = f"/tmp/{repo_name}"

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



    filetool_git_repo_tree_input = {
            "git_repo_path": repo_path
        }
    filetool_git_repo_tree_output = composio_toolset.execute_action(
        action=Action.FILETOOL_GIT_REPO_TREE,
        params=filetool_git_repo_tree_input
    )
    print("FILETOOL_GIT_REPO_TREE")
    print(filetool_git_repo_tree_input)
    print(json.dumps(filetool_git_repo_tree_output['data'], indent=4, sort_keys=True))
    print("===================================================")

    filetool_list_files_input = {}
    filetool_list_files_output = composio_toolset.execute_action(
        action=Action.FILETOOL_LIST_FILES,
        params={}
    )
    print("FILETOOL_LIST_FILES")
    print(filetool_list_files_input)
    print(json.dumps(filetool_list_files_output['data'], indent=4, sort_keys=True))
    print("===================================================")

    filetool_open_file_input = {
        "file_path": "termin_api.py",
        "line_number": 5
    }
    filetool_open_file_output = composio_toolset.execute_action(
        action=Action.FILETOOL_OPEN_FILE,
        params=filetool_open_file_input,
    )
    print("FILETOOL_OPEN_FILE")
    print(filetool_open_file_input)
    print(json.dumps(filetool_open_file_output['data'], indent=4, sort_keys=True))
    print("===================================================")

    filetool_scroll_input = {
        "direction": "down",
        "lines": 10
    }
    filetool_scroll_output = composio_toolset.execute_action(
        action=Action.FILETOOL_SCROLL,
        params=filetool_scroll_input,
    )
    print("FILETOOL_SCROLL")
    print(filetool_scroll_input)
    print(json.dumps(filetool_scroll_output['data'], indent=4, sort_keys=True))
    print("===================================================")

    filetool_edit_file_input = {
        "file_path": "termin_api.py",
        "text": "# super cool comment!",
        "start_line": 8,
        "end_line": 8
    }
    filetool_edit_file_output = composio_toolset.execute_action(
        action=Action.FILETOOL_EDIT_FILE,
        params=filetool_edit_file_input,
    )
    print("FILETOOL_EDIT_FILE")
    print(filetool_edit_file_input)
    print(json.dumps(filetool_edit_file_output['data'], indent=4, sort_keys=True))
    print("===================================================")
    filetool_create_file_input = {
        "path": "new_file.py",
        "is_directory": False,
    }
    filetool_create_file_output = composio_toolset.execute_action(
        action=Action.FILETOOL_CREATE_FILE,
        params=filetool_create_file_input,
    )
    print("FILETOOL_CREATE_FILE")
    print(filetool_create_file_input)
    print(json.dumps(filetool_create_file_output['data'], indent=4, sort_keys=True))
    print("===================================================")

    filetool_find_file_input = {
        "pattern": ".*file",
        "depth": 1,
        "case_sensitive": False,
        "include": [],
        "exclude": [],
    }
    filetool_find_file_output = composio_toolset.execute_action(
        action=Action.FILETOOL_FIND_FILE,
        params=filetool_find_file_input,
    )
    print("FILETOOL_FIND_FILE")
    print(filetool_find_file_input)
    print(json.dumps(filetool_find_file_output['data'], indent=4, sort_keys=True))
    print("===================================================")


    filetool_search_word_input = {
        "word": "termin",
        "pattern": "*.py",
        "recursive": True,
        "case_insensitive": True,
        "exclude": [],
    }
    filetool_search_word_output = composio_toolset.execute_action(
        action=Action.FILETOOL_SEARCH_WORD,
        params=filetool_search_word_input,
    )
    print("FILETOOL_SEARCH_WORD")
    print(filetool_search_word_input)
    print(json.dumps(filetool_search_word_output['data'], indent=4, sort_keys=True))
    print("===================================================")


    filetool_write_input = {
        "file_path": "new_file.py",
        "text": "Super text!",
    }
    filetool_write_output = composio_toolset.execute_action(
        action=Action.FILETOOL_WRITE,
        params=filetool_write_input,
    )
    print("FILETOOL_WRITE")
    print(filetool_write_input)
    print(json.dumps(filetool_write_output['data'], indent=4, sort_keys=True))
    print("===================================================")


    filetool_git_patch_input = {
        "new_file_paths": ["new_file.py",],
    }
    filetool_git_patch_output = composio_toolset.execute_action(
        action=Action.FILETOOL_GIT_PATCH,
        params=filetool_git_patch_input,
    )
    print("FILETOOL_GIT_PATCH")
    print(filetool_git_patch_input)
    print(json.dumps(filetool_git_patch_output['data'], indent=4, sort_keys=True))
    print("===================================================")




    code_analysis_tool_get_class_info_input = {
        "class_name": "ForeignLabor",
    }
    code_analysis_tool_get_class_info_output = composio_toolset.execute_action(
        action=Action.CODE_ANALYSIS_TOOL_GET_CLASS_INFO,
        params=code_analysis_tool_get_class_info_input,
    )
    print("CODE_ANALYSIS_TOOL_GET_CLASS_INFO")
    print(code_analysis_tool_get_class_info_input)
    print(json.dumps(code_analysis_tool_get_class_info_output['data'], indent=4, sort_keys=True))
    print("===================================================")

    code_analysis_tool_get_method_body_input = {
        "class_name": "ForeignLabor",
        "method_name": "get_name",
    }
    code_analysis_tool_get_method_body_output = composio_toolset.execute_action(
        action=Action.CODE_ANALYSIS_TOOL_GET_METHOD_BODY,
        params=code_analysis_tool_get_method_body_input,
    )
    print("CODE_ANALYSIS_TOOL_GET_METHOD_BODY")
    print(code_analysis_tool_get_method_body_input)
    print(json.dumps(code_analysis_tool_get_method_body_output['data'], indent=4, sort_keys=True))
    print("===================================================")

    code_analysis_tool_get_method_signature_input = {
        "class_name": "ForeignLabor",
        "method_name": "get_name",
    }
    code_analysis_tool_get_method_signature_output = composio_toolset.execute_action(
        action=Action.CODE_ANALYSIS_TOOL_GET_METHOD_SIGNATURE,
        params=code_analysis_tool_get_method_signature_input,
    )
    print("CODE_ANALYSIS_TOOL_GET_METHOD_SIGNATURE")
    print(code_analysis_tool_get_method_signature_input)
    print(json.dumps(code_analysis_tool_get_method_signature_output['data'], indent=4, sort_keys=True))
    print("===================================================")




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
