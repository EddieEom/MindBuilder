"""
Reserved for Local Transformer Provider.

(Current provider : OpenRouter)
"""

# from transformers import (
#     AutoModelForCausalLM,
#     AutoTokenizer,
# )

# from app.ai.llm.config import (
#     MODEL_NAME,
#     MODEL_CACHE,
#     DEVICE,
#     DTYPE,
# )


# class LLMLoader:

#     _tokenizer = None
#     _model = None

#     @classmethod
#     def get_tokenizer(cls):

#         if cls._tokenizer is None:

#             print("[LLM] Loading tokenizer...")

#             cls._tokenizer = AutoTokenizer.from_pretrained(

#                 MODEL_NAME,

#                 cache_dir=MODEL_CACHE,

#                 trust_remote_code=True,

#             )

#             print("[LLM] Tokenizer loaded.")

#         return cls._tokenizer

#     @classmethod
#     def get_model(cls):

#         if cls._model is None:

#             print("[LLM] Loading model...")

#             cls._model = AutoModelForCausalLM.from_pretrained(

#                 MODEL_NAME,

#                 cache_dir=MODEL_CACHE,

#                 torch_dtype=DTYPE,

#                 device_map=DEVICE,

#                 trust_remote_code=True,

#             )

#             cls._model.eval()

#             print("[LLM] Model loaded.")

#         return cls._model