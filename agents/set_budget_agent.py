from mcptool.tool_manager import ToolManager

#creating class based agent

class SetBudgetAgent:
    TOOL_NAME="set_budget"

    def __init__(self,tool_manager:ToolManager):
        self._tool_manager=tool_manager
        
    
    def handle(self,arguments:dict):
        result=self._tool_manager.execute(self.TOOL_NAME,arguments)
        return {"tool_name":self.TOOL_NAME,"arguments":arguments,"result":result}