from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser
from langchain.schema.output import LLMResult
from langchain.schema.messages import BaseMessage, SystemMessage, HumanMessage
from langchain.schema.agent import AgentAction, AgentFinish

from typing import Any, Dict, List, Optional, Sequence, Union
from uuid import UUID
import logging
import time
from cost_estimator import get_openai_token_cost_for_model, MODEL_COST_PER_1K_TOKENS

class Run:
    def __init__(self, parent_id: Optional[str] = None, debug: bool = False) -> None:
        self.parent_id = parent_id
        self.runs = {}
        self.function_calls = {}
        self.output_dict = {} # New dict to log function calls
        if debug:
            logging.basicConfig()
            self.log = logging.getLogger('Run')
            self.log.setLevel(logging.DEBUG)
        else:
            self.log = logging.getLogger('Run')
            self.log.setLevel(logging.WARNING)

    def log_run(self, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> None:
        run_info = {
            'run_id': run_id,
            'parent_run_id': parent_run_id,
            'start_time': kwargs.get('start_time', None),
            'end_time': kwargs.get('end_time', None),
            'outputs': kwargs.get('outputs', None),
            'inputs': kwargs.get('inputs', None),
            'token': kwargs.get('token', None),
            'error': kwargs.get('error', None),
        }
        # Remove None values
        run_info = {k: v for k, v in run_info.items() if v is not None}
        self.runs[run_id] = run_info

class CallbackHandler(BaseCallbackHandler):
    def __init__(self, magik_api_key: Optional[str] ) -> None:
        self.run = Run(debug=True) # Create a single instance of Run
        self.magik_api_key = magik_api_key
        self.output_dict = {} 
        
    def get_runs(self):
        return self.run.runs 
    
    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any, 
    ) -> Any:
        print("on_chat_model_start called")
        start_time = time.time() 
        print("\n Serialized:", serialized)
        print("\n Messages:", messages)
        print("\nkwargs:", kwargs)
        print("\n start time:", start_time)
        flattened_messages = [message for sublist in messages for message in sublist]  # Flatten the list of messages
        user_query = ' '.join([message.content for message in flattened_messages if isinstance(message, HumanMessage)])  # Combine human messages
        language_model_id = kwargs['invocation_params']['model']  # Get the model ID
        prompt_sent = ' '.join([str(message) for message in flattened_messages])  # Combine system and human messages
        # Create a new dict with the required information
        self.run_info.update = {
            'user_query': user_query,
            'start_time': start_time,
            'language_model_id': language_model_id,
            'prompt_sent': prompt_sent
        }
        print("\nLLM start:" ,self.run_info)
        self.run.log_run(run_id, parent_run_id, serialized=serialized, messages=messages, start_time=start_time)
        self.run.function_calls[run_id] = 'on_chat_model_start'  # Log the function call
        self.run.runs[run_id].update(self.run_info)   

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], run_id: UUID, parent_run_id: Optional[UUID] = None,**kwargs: Any
    ) -> Any:
        print("on_chain_start called")
        print("\n Serialized:", serialized)
        print("\n Inputs", inputs)
        print("\nkwargs:", kwargs)
        start_time = time.time()
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, serialized=serialized, inputs=inputs, start_time=start_time)
        self.run.function_calls[run_id] = 'on_chain_start'  # Log the function call
        self.runs[run_id] = self.run.runs[run_id]  # Store the run dict in self.runs

    def on_chain_end(self, outputs: Dict[str, Any], run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("on_chain_end called")
        end_time = time.time()
        print("\nOutputs:", outputs)
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, outputs=outputs, end_time=end_time)
        self.run.function_calls[run_id] = 'on_chain_end'  # Log the function call
        self.runs[run_id] = self.run.runs[run_id]  # Store the run dict in self.runs

    def on_chat_model_end(self, outputs: Dict[str, Any], run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("on_chat_model_end called")
        end_time = time.time()
        print("\n on chat model end")
        print("\nOutputs:", outputs)
        print("\nkwargs:", kwargs)
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, outputs=outputs, end_time=end_time)
        self.run.function_calls[run_id] = 'on_chat_model_end'  # Log the function call
        self.run.runs[run_id] = self.run.runs[run_id]  # Store the run dict in self.runs

    # def on_llm_end(self, response: LLMResult, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
    #     print("on_llm_end called")
    #     end_time = time.time()
    #     token_usage = response.llm_output['token_usage']
    #     prompt_tokens = token_usage['prompt_tokens']
    #     completion_tokens = token_usage['completion_tokens']
    #     total_tokens = token_usage['total_tokens']
    #     prompt_completion = ', '.join([gen.text for gen in response.generations[0]])  # Join the prompt completions with a comma
    #     print("\nExecuting: on_llm_end")
    #     print("\nresponse:", response)
    #     print("\nkwargs:", kwargs)
    #     # Update the output dictionary with the required information
    #     self.output_dict.update({
    #         'prompt_response': prompt_completion,
    #         'response_time': end_time - self.output_dict['start_time'],
    #         'prompt_tokens': prompt_tokens,
    #         'completion_tokens': completion_tokens,
    #         'total_tokens': total_tokens,
    #     })
    #     print("\nFinal output:", self.output_dict)
        # return self.output_dict
    def on_llm_end(self, response: LLMResult, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        end_time = time.time()
        token_usage = response.llm_output['token_usage']
        prompt_tokens = token_usage['prompt_tokens']
        completion_tokens = token_usage['completion_tokens']
        total_tokens = token_usage['total_tokens']
        prompt_completion = ', '.join([gen.text for gen in response.generations[0]])  # Join the prompt completions with a comma

        # Create a new dict with the required information
        self.run_info.update = {
            'prompt_response': prompt_completion,
            'completion_tokens': completion_tokens,
            'prompt_tokens': prompt_tokens,
            'total_tokens': total_tokens,
            'end_time': end_time
        }
        print("\nLLM END:" ,self.run_info)
        # Store the run dict in self.runs
        self.run.runs[run_id].update(self.run_info)

    # def on_llm_start(
    #     self, serialized: Dict[str, Any], prompts: List[str], run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any
    # ) -> Any:
    #     start_time = time.time()
    #     user_query = prompts[0]  # Assuming the first prompt is the user query
    #     print("\nExecuting: on_llm_start")
    #     print("\nSerialized:", serialized)
    #     print("\nPrompts:", prompts)
    #     # Store the user query and start time in the output dictionary
    #     self.output_dict['user_query'] = user_query
    #     self.output_dict['start_time'] = start_time
    #     self.output_dict['prompt_sent'] = serialized['prompt']  # Assuming 'prompt' key in serialized dict
    #     self.output_dict['language_model_id'] = serialized['model_name']  # Assuming 'model' key in serialized dict        
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("on_llm_start method called")
        
        start_time = time.time()
        user_query = prompts[0]  # Assuming the first prompt is the user query

        # Create a new dict with the required information
        run_info = {
            'user_query': user_query,
            'start_time': start_time
        }
        print("\nLLM START:" ,run_info)
        # Store the run dict in self.runs
        self.runs[run_id] = run_info  # Log the function call

    def on_llm_new_token(self, token: str, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("\nExecuting: on_llm_new_token")
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, token=token)
        self.run.function_calls[run_id] = 'on_llm_new_token'  # Log the function call

    def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("\nExecuting: on_llm_error")
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, error=error)
        self.run.function_calls[run_id] = 'on_llm_error'  # Log the function call

    def on_chain_error(self, error: Union[Exception, KeyboardInterrupt], run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("\nExecuting: on_chain_error")
        self.run.runs = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, error=error)
        self.run.function_calls[run_id] = 'on_chain_error'  # Log the function call
    
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("\nExecuting: on_tool_start")
        start_time = time.time()
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, serialized=serialized, input_str=input_str, start_time=start_time)
        run.function_calls[run_id] = 'on_tool_start'  # Log the function call

    def on_tool_end(self, output: str, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("\nExecuting: on_tool_end")
        end_time = time.time()
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, output=output, end_time=end_time)
        run.function_calls[run_id] = 'on_tool_end'  # Log the function call

    def on_tool_error(self, error: Union[Exception, KeyboardInterrupt], run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("\nExecuting: on_tool_error")
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, error=error)
        run.function_calls[run_id] = 'on_tool_error'  # Log the function call

    # def on_text(self, text: str, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
    #     # Store the user query in the output dictionary
    #     self.output_dict['user_query'] = text
    #     print("\nExecuting: on_text")
    #     print("\nText:", text)
    def on_text(self, text: str, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("\nExecuting: on_text")
        print("\nText:", text)
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, text=text)
        run.function_calls[run_id] = 'on_text'  # Log the function call

    def on_agent_action(self, action: AgentAction, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("\nExecuting: on_agent_action")
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, action=action)
        run.function_calls[run_id] = 'on_agent_action'  # Log the function call
        
    def on_agent_finish(self, finish: AgentFinish, run_id: UUID, parent_run_id: Optional[UUID] = None, **kwargs: Any) -> Any:
        print("\nExecuting: on_agent_finish")
        run = Run(parent_id=parent_run_id, debug=True)
        self.run.log_run(run_id, parent_run_id, finish=finish)
        run.function_calls[run_id] = 'on_agent_finish'  # Log the function call

class CommaSeparatedListOutputParser(BaseOutputParser):
    """Parse the output of an LLM call to a comma-separated list."""

    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")

template = """You are a helpful assistant who generates comma separated lists.
A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.
ONLY return a comma separated list, and nothing more."""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)


chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt])

handler = CallbackHandler(magik_api_key="QNPKZp1q97kMfSIPoS6_1eNpllOU3l3a")

chain = LLMChain(
    llm=ChatOpenAI(
        openai_api_key="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"),
    prompt=chat_prompt,
    output_parser=CommaSeparatedListOutputParser()
)
print(chain.run("Give me a list of 5 bugattis", callbacks=[handler]))



