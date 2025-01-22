import { CreateServiceWorkerMLCEngine, MLCEngineInterface } from "@mlc-ai/web-llm";

if( 'serviceWorker' in navigator){
  navigator.serviceWorker.register(new URL('sw.ts',import.meta.url),{type:'module'}).then((reg)=>{
    console.log('service worker registered:',reg)
  }).catch((er)=>{
    console.error('service worker registration failed',er);
  })
}



async function createModelEnginer(model:string) {


  const modelVersion = "v0_2_48";
const modelLibURLPrefix =
  "https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/web-llm-models/";


  const enginer: MLCEngineInterface = await CreateServiceWorkerMLCEngine(
    model,
    {
      appConfig:{
        useIndexedDBCache:true,
        model_list:[
          {
            model:
              "https://huggingface.co/mlc-ai/DeepSeek-R1-Distill-Qwen-7B-q4f16_1-MLC",
            model_id: "DeepSeek-R1-Distill-Qwen-7B-q4f16_1-MLC",
            model_lib:
              modelLibURLPrefix +
              modelVersion +
              "/Qwen2-7B-Instruct-q4f16_1-ctx4k_cs1k-webgpu.wasm",
            low_resource_required: false,
            vram_required_MB: 5106.67,
            overrides: {
              context_window_size: 4096,
            },
          },  {
            model:
              "https://huggingface.co/mlc-ai/Mistral-7B-Instruct-v0.3-q4f16_1-MLC",
            model_id: "Mistral-7B-Instruct-v0.3-q4f16_1-MLC",
            model_lib:
              modelLibURLPrefix +
              modelVersion +
              "/Mistral-7B-Instruct-v0.3-q4f16_1-ctx4k_cs1k-webgpu.wasm",
            vram_required_MB: 4573.39,
            low_resource_required: false,
            required_features: ["shader-f16"],
            overrides: {
              context_window_size: 4096,
              sliding_window_size: -1,
            },
          },  {
            model:
              "https://huggingface.co/mlc-ai/OpenHermes-2.5-Mistral-7B-q4f16_1-MLC",
            model_id: "OpenHermes-2.5-Mistral-7B-q4f16_1-MLC",
            model_lib:
              modelLibURLPrefix +
              modelVersion +
              "/Mistral-7B-Instruct-v0.3-q4f16_1-ctx4k_cs1k-webgpu.wasm",
            vram_required_MB: 4573.39,
            low_resource_required: false,
            required_features: ["shader-f16"],
            overrides: {
              context_window_size: 4096,
              sliding_window_size: -1,
            },
          },
          {
            model: "https://huggingface.co/mlc-ai/Hermes-3-Llama-3.2-3B-q4f16_1-MLC",
            model_id: "Hermes-3-Llama-3.2-3B-q4f16_1-MLC",
            model_lib:
              modelLibURLPrefix +
              modelVersion +
              "/Llama-3.2-3B-Instruct-q4f16_1-ctx4k_cs1k-webgpu.wasm",
            vram_required_MB: 2263.69,
            low_resource_required: true,
            overrides: {
              context_window_size: 4096,
            },
          },
        ]
      }
    }
  )
}