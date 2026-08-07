# from transformers import (
#     AutoTokenizer,
#     AutoModelForCausalLM,
# )

# import torch


# class LLMService:

#     def __init__(
#         self,
#         model_name: str = "Qwen/Qwen3-8B-Instruct",
#     ):

#         self.tokenizer = AutoTokenizer.from_pretrained(
#             model_name,
#             trust_remote_code=True,
#         )

#         self.model = AutoModelForCausalLM.from_pretrained(
#             model_name,
#             torch_dtype=torch.bfloat16,
#             device_map="auto",
#             trust_remote_code=True,
#         )

#     def generate(
#         self,
#         system_prompt: str,
#         user_prompt: str,
#         temperature: float = 0.6,
#         max_new_tokens: int = 1024,
#     ) -> str:

#         messages = [

#             {
#                 "role": "system",
#                 "content": system_prompt,
#             },

#             {
#                 "role": "user",
#                 "content": user_prompt,
#             },

#         ]

#         text = self.tokenizer.apply_chat_template(
#             messages,
#             tokenize=False,
#             add_generation_prompt=True,
#         )

#         inputs = self.tokenizer(
#             text,
#             return_tensors="pt",
#         ).to(
#             self.model.device
#         )

#         outputs = self.model.generate(
#             **inputs,
#             max_new_tokens=max_new_tokens,
#             temperature=temperature,
#         )

#         return self.tokenizer.decode(
#             outputs[0],
#             skip_special_tokens=True,
#         )