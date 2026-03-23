import requests
import json
import os
import shutil

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

NASA_KEY = os.environ.get("NASA_API_KEY") or "G2zfhr9fNf26KgAMWoMPiNlgNATaArYPADehWjTw"
resultado_final = {}

for tarefa in config["tarefas"]:
    print(f"Processando: {tarefa['nome']}")
    
    params = {"api_key": NASA_KEY}
    response = requests.get(tarefa["api_url"], params=params)
    
    if response.status_code == 200:
        dados_brutos = response.json()
        dados_filtrados = {}
        
        for chave in tarefa["chaves"]:
            if chave in dados_brutos:
                dados_filtrados[chave] = dados_brutos[chave]
        
        resultado_final[tarefa["nome"]] = dados_filtrados

        if tarefa.get("baixar_arquivo") and "url" in dados_filtrados:
            img_res = requests.get(dados_filtrados["url"], stream=True)
            if img_res.status_code == 200:
                nome_img = f"{tarefa['nome']}.jpg"
                with open(nome_img, "wb") as f_img:
                    shutil.copyfileobj(img_res.raw, f_img)
                print(f"Arquivo baixado: {nome_img}")

with open(config["arquivo_final"], "w", encoding="utf-8") as f_out:
    json.dump(resultado_final, f_out, indent=4, ensure_ascii=False)

print(f"\nRelatório completo salvo em: {config['arquivo_final']}")