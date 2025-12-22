from typing import List, Optional, Dict, Tuple, AsyncGenerator, Any, Generator
from dataclasses import dataclass
from agents import RunResultStreaming, ItemHelpers

@dataclass(frozen=True)
class CustomMessage:
    tool_name: str
    message: str
    is_call: bool = True
    is_output: bool = False

    def format_message(self, output: Optional[str] = None) -> str:
        data = {"tool_name" : self.tool_name}
        if self.is_output and output is not None:
            data["output"] = output
        
        try:
            return self.message.format(**data)
        except KeyError:
            return self.message

class StatusStreaming:
    def __init__(self, custom_messages: Optional[List[CustomMessage]] = None, use_default: bool = True, show_raw_output : bool=False, show_agent_switch : bool = True):
        self.tool_stack: List[str] = []
        self.use_default = use_default
        self.show_raw_output = show_raw_output
        self.show_agent_switch = show_agent_switch

        if custom_messages is None: 
            custom_messages = []

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
        - status: Mensagens de ferramentas
        - content: Resposta final do LLM 
        """
        async for event in stream.stream_events():
            match event.type:
                case "agent_updated_stream_event":
                    if self.show_agent_switch:
                        yield ("agent_switch", F"Transferindo para {event.new_agent.name}")
                
                case "run_item_stream_event":
                    match event.item.type:
                        case "tool_call_item":
                            for msg in self._handle_tool_call(event.item):
                                yield msg
                        case "tool_call_output_item":
                            for msg in self._handle_tool_output(event.item):
                                yield msg
                        case "message_output_item":
                            content = ItemHelpers.text_message_output(event.item)
                            if content:
                                yield ("content", content)
    
        
    def _handle_tool_call(self, item : Any) -> Generator[Tuple[str, str], None]:
        tool_name = item.raw_item.name
        self.tool_stack.append(tool_name)

        msg_obj = self._get_message_obj(tool_name ,"call")

        if msg_obj:
            yield ("status", msg_obj.format_message())
        elif self.use_default:
            yield ("status", f"Chamando ferramenta: {tool_name}....")
    
    def _handle_tool_output(self, item : Any) -> Generator[Tuple[str, str], None]:
        if not self.tool_stack:
            return
        
        tool_name = self.tool_stack.pop()
        output_str = str(item.output)

        msg_obj = self._get_message_obj(tool_name, "output")

        if msg_obj:
            yield ("status", msg_obj.format_message(output=output_str))
        elif self.use_default and self.show_raw_output:
            yield ("status", f"Output de {tool_name}: {output_str}")
        