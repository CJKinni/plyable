import openai
import time

class Plyable:
    _on_input_message = []
    _on_output_message = []
    _validate_output_message = []
    _validate_input_message = []
    
    @classmethod
    def on_input_message(cls, func):
        cls._on_input_message.append(func)
        return func

    @classmethod
    def on_output_message(cls, func):
        cls._on_output_message.append(func)
        return func

    @classmethod
    def validate_output_message(cls, func):
        cls._validate_output_message.append(func)
        return func

    @classmethod
    def validate_input_message(cls, func):
        cls._validate_input_message.append(func)
        return func

    @classmethod
    def input_validation_error(cls, func):
        cls._input_validation_error = func
        return func

    def _initialize_system_message(self):
        self.message_log = [self._fmt_msg("system", self.system_message)]
        
    def update_openai_api_key(self, openai_api_key):
        openai.api_key = openai_api_key

    def __init__(self, system_message = "You are a chat bot", retries=3, gpt_version='gpt-3.5-turbo', openai_api_key=None):
        self.system_message = system_message
        self.message_log = None
        self.retries = retries
        self.gpt_version = gpt_version
        self.rate_limit_retry_enabled = True
        self.rate_limit_retry_timeout = 25
        self.rate_limit_retries = 5
        if openai_api_key is not None:
            self.update_openai_api_key(openai_api_key)
        
        
    def _append_to_log(self, role, message):
        if self.message_log is None:
            self._initialize_system_message()

        self.message_log.append(self._fmt_msg(role, message))

    def send(self, message, retries=None):
        if retries is None:
            retries = self.retries

        # If on_input_message returns a value, we use that as a replacement for the message
        for func in self._on_input_message:
            response = func(self, message)
            if response:
                message = response

        in_validations = [func(self, message) for func in self._validate_input_message]
        failed_validations = [validation for validation in in_validations if validation and validation[0] == False]
        if len(failed_validations) > 0:
            all_errors = [validation[1] for validation in failed_validations]
            prose_errors = '. '.join(all_errors)
            self._append_to_log("system", prose_errors)
            return prose_errors
        
        self._append_to_log("user", message)
        llm_response = self._get_llm_response()
        if llm_response is None:
            return None
        
        # Validate response
        llm_response_message = llm_response.choices[0].get('message')
        llm_response_content = llm_response_message.get('content')
        self.message_log.append(llm_response_message)

        out_validations = [func(self, llm_response_content) for func in self._validate_output_message]
        failed_validations = [validation for validation in out_validations if validation and validation[0] == False]
        if len(failed_validations) > 0:
            if retries > 0:
                all_errors = [validation[1] for validation in failed_validations]
                prose_errors = '. '.join(all_errors)
                self._append_to_log("user", prose_errors)
                return self.send(message, retries=retries-1)
            else:
                return None

        [func(self, llm_response_content) for func in self._on_output_message]
        return llm_response_content

    def _get_llm_response(self, retries=0):
        try:
            completion = openai.ChatCompletion.create(
                        model=self.gpt_version, 
                        messages=self.message_log,
                    )
            return completion
        except openai.error.RateLimitError as e:
            if self.rate_limit_retry_enabled and retries < self.rate_limit_retries:
                print("Rate limit error. waiting to try again.")
                time.sleep(self.rate_limit_retry_timeout)
                return self._get_llm_response(retries=retries+1)
            return None
        except openai.error.AuthenticationError as e:
            print("OpenAPI Authentication Error. Please verify your API key.")
            return None
            
                

    def _fmt_msg(self, role, input):
        return {
                'role': role,
                'content': input
            }
    