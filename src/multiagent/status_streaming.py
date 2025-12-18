from typing import List, Optional, Dict, Tuple, AsyncGenerator
from dataclasses import dataclass
from agents import RunResultStreaming, ItemHelpers

@dataclass
class CustomMessage:
    tool_name: str
    message: str
    is_call: bool = True
    is_output: bool = False
    result: Optional[str] = None 

    @property
    def formatted_message(self) -> str:
        data = {"tool_name": self.tool_name}
        if self.is_output and self.result is not None:
            data["output"] = self.result
        return self.message.format(**data)

class StatusStreaming:
    def __init__(self, custom_messages: List[CustomMessage] = [], show_raw: bool = False, show_raw_output=True):
        self.tool_stack: List[str] = []
        self.show_raw = show_raw
        self.show_raw_output = show_raw_output
        
        # (tool_name, "call"|"output")
        self.message_map: Dict[Tuple[str, str], CustomMessage] = {}
        for msg in custom_messages:
            msg_type = "output" if msg.is_output else "call"
            self.message_map[(msg.tool_name, msg_type)] = msg

    def _get_message_obj(self, tool_name: str, msg_type: str) -> Optional[CustomMessage]:
        return self.message_map.get((tool_name, msg_type))

    async def process_stream(self, stream: RunResultStreaming) -> AsyncGenerator[Tuple[str, str], None]:
        """
        retorna (tipo_evento, conteudo_formatado)
        
        tipos:
        - agent_switch: Mudança de agente
        - status: Mensagens de ferramentas (call/output)
        - content: Resposta final do LLM (tokens ou texto completo)
        """
        async for event in stream.stream_events():
            
            if event.type == "agent_updated_stream_event":
                yield ("agent_switch", f"Transferindo para o {event.new_agent.name}")

            elif event.type == "run_item_stream_event":
                item = event.item

                if item.type == "tool_call_item":
                    tool_name = item.raw_item.name
                    self.tool_stack.append(tool_name)
                    
                    msg_obj = self._get_message_obj(tool_name, "call")
                    
                    if msg_obj:
                        yield ("status", msg_obj.formatted_message)
                    elif self.show_raw:
                        yield ("status", f"Chamando ferramenta: {tool_name}...")

                elif item.type == "tool_call_output_item":
                    if self.tool_stack:
                        tool_name = self.tool_stack.pop()
                        output_str = str(item.output)
                        
                        msg_obj = self._get_message_obj(tool_name, "output")
                        
                        if msg_obj:
                            msg_obj.result = output_str
                            yield ("status", msg_obj.formatted_message)
                            msg_obj.result = None
                        elif self.show_raw and self.show_raw_output:
                            yield ("status", f"Output de {tool_name}: {output_str}")

                elif item.type == "message_output_item":
                    content = ItemHelpers.text_message_output(item)
                    if content:
                        yield ("content", content)