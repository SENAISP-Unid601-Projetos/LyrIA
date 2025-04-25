from src.ia import LyrIA
import random

def main():
    ia = LyrIA()
    print("\nLyrIA: Olá! Sou a LyrIA, sua assistente. Como posso ajudar? (Digite 'sair' para encerrar)")
    
    while True:
        try:
            pergunta = input("\nVocê: ")
            if pergunta.lower() in ['sair', 'tchau', 'adeus']:
                print(f"\nLyrIA: {random.choice(ia.dialogs['despedidas'])}")
                break
                
            resposta = ia.responder(pergunta)
            print(f"\nLyrIA: {resposta}")
            
        except KeyboardInterrupt:
            print("\nLyrIA: Até logo! Foi bom conversar com você!")
            break

if __name__ == "__main__":
    main()