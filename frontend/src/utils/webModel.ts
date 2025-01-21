import { CreateServiceWorkerMLCEngine, MLCEngineInterface } from "@mlc-ai/web-llm";

if( 'serviceWorker' in navigator){
  navigator.serviceWorker.register(new URL('sw.ts',import.meta.url),{type:'module'}).then((reg)=>{
    console.log('service worker registered:',reg)
  }).catch((er)=>{
    console.error('service worker registration failed',er);
  })
}

const modelVersion = "v0_2_48";
const modelLibURLPrefix =
  "https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/web-llm-models/";


async function getResponce(model) {
  const enginer: MLCEngineInterface = await CreateServiceWorkerMLCEngine(
    model,
    {
      appConfig:{
        useIndexedDBCache:true,
        model_list:[
          {
            model: "https://huggingface.co/mlc-ai/Llama-3.2-1B-Instruct-q4f32_1-MLC",
            model_id: "Llama-3.2-1B-Instruct-q4f32_1-MLC",
            model_lib:
              modelLibURLPrefix +
              modelVersion +
              "/Llama-3.2-1B-Instruct-q4f32_1-ctx4k_cs1k-webgpu.wasm",
            vram_required_MB: 1128.82,
            low_resource_required: true,
            overrides: {
              context_window_size: 4096,
            },
          }
        ]
      }
    }
  )
}