import car_crash_analysis
import os


def start_prompt():
    plots = car_crash_analysis.get_functions()
    
    while True:
        
        flag = True
            
        print("Naudokite nuo 1-8 skaičius. Apačioje rašo, kas ką reiškia.")
        print()
        print("1. Avarijų bei mirčių kiekis per metus;")
        print("2. Moterų bei vyrų patekusiu į avariją procentai;")
        print("3. Aplinkinių priežasčių dažniausiai pasitaikanti kombinacija;")
        print("4. Girtų vairuotojų duomenys;")
        print("5. Ket taisyklių pažeidimai;")
        print("6. Išsaugoti nuotraukas;")
        print("7. Atspausdinti duomenis(xlsx, csv);")
        print("8. Išeiti;")
        user_input = input("Kaip norėtumėte elgtis?: ")
        
        for plot in plots:
            if user_input == plot[0]:
                if user_input == "7":
                    save_to_spreadsheet(plot)
                else:
                    plot[1](*plot[2])
                flag = False
                break
        os.system('cls' if os.name == 'nt' else 'clear')   
        if user_input == "6":
            save_pic_prompt(plots)
        elif user_input == "8":
            break
        elif flag:
            print("Nėra tokio pasirinkimo, bandykite dar karta.")

            
def save_spreadsheet_prompt(plot):
    invalid = False
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        if invalid:
            print("Nėra tokio pasirinkimo, bandykite dar karta.")
            invalid = False    
        user_input = input("Norėtum kaip excel ar kaip csv failą išsaugoti?(E/CSV): ")
        if user_input.lower() == "e":
            plot[1](*plot[2], to_excel=True)
            break
        elif user_input.lower() == "csv":
            plot[1](*plot[2]) 
            break   
        else:
            invalid = True 
                
def save_pic_prompt(plots):
    while True:
        
        flag = True
            
        print("Naudokite nuo 1-8 skaičius. Apačioje rašo, kas ką reiškia.")
        print()
        print("1. Išsaugoti avarijų bei mirčių kiekio per metus grafiką;")
        print("2. Išsaugoti moterų bei vyrų patekusiu į avariją grafiką;")
        print("3. Išsaugoti aplinkinių priežasčių dažniausiai pasitaikančių kombinacijų grafiką;")
        print("4. Išsaugoti girtų vairuotojų duomenų grafiką;")
        print("5. Išsaugoti ket taisyklių pažeidimų lentelę;")
        print("6. Išsaugoti visus grafikus;")
        print("7. Grižti atgal;")
        user_input = input("Kaip norėtumėte elgtis?: ")
        
        if user_input == "7":
            break
        
        for index, plot in enumerate(plots):
            if user_input == "6":
                flag = False
                plot[1](*plot[2], to_png=True)
                if len(plots)-2==index:
                    break
            if user_input == plot[0]:
                plot[1](*plot[2], to_png=True)
                flag = False
                break
            
        os.system('cls' if os.name == 'nt' else 'clear')    
        if flag:
            print("Nėra tokio pasirinkimo, bandykite dar karta.")
        
