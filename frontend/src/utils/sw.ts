import { ServiceWorkerMLCEngineHandler } from "@mlc-ai/web-llm"


self.addEventListener(
    'activate',()=>{
        const handler = new ServiceWorkerMLCEngineHandler()
    }
)

self.addEventListener(
    'fetch',(event)=>{
        if (event.request.url.includes('/models/')) {
            event.respondWith(handleModelRequest(event.request));
        } else {
            event.respondWith(fetch(event.request)); // Handle other requests normally
        }
    }
)


async function handleModelRequest(request: Request){
    const modelId = new URL(request.url).pathname.split('/').pop();
    const cachedModel = await caches.match(request);

    if(cachedModel){
        return cachedModel
    }

    const res=await fetch(request)
    const modelData = res.blob();

    const cache = await fetch(request);
    cache.put(request.url,new Response(modelData))

    return res
}