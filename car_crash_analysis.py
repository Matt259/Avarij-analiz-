import pandas as pd
import numpy as np
from json_reader import JSONReader
import matplotlib.pyplot as plt
import os
import re

#prompts the json_reader, loads the data into a dataframe and cleans it up.
def return_cleaned_df():

    cwd = os.getcwd()
    change_json_name(cwd)
         
    dict_list = []
    for file in os.listdir(cwd):
        if file.startswith("accidents_") and file.endswith(".json"):
            accident = JSONReader(file, int(file.split("_")[1].split(".")[0]))
            dict_list.append(pd.DataFrame(accident.filter_data()))

    #concat all the json files into a single dataframe
    df = pd.concat(dict_list)
    # df['driver_age'] = df['driver_age'].astype('int64')
    #replace empty values and nan
    df = df.replace(['', np.nan], "Nežinoma")
    #strip whitespace 
    df['time_of_day'] = df['time_of_day'].str.strip()
    
    return df

def change_json_name(cwd):
    pattern = re.compile(r'accidents_[0-9]{4}\.json')
    #rename the initial files
    for file in os.listdir(cwd):
        if file.endswith(".json") and not pattern.match(file):
            new_file_name = "accidents_" + file.split('_')[1].split()[0] + ".json"
            os.rename(os.path.join(cwd, file), os.path.join(cwd, new_file_name))
            
#Gets all the years. In other words all the years that are getting analized
def get_unique_years(df):
    return df["year"].unique()

#Gets lowest and highest year
def get_years_from_to(unique_years):
    return str(unique_years[0]) + "-" + str(unique_years[-1])


#csv and xlsx writer. If true writes to an xlsx if false to multiple csv files
def df_writer(df, unique_years, years_from_to, to_excel = False):
    df.columns = ("Metai","Incidento ID", "Vairuotojo amžius", "Vairuotojo lytis", "Vairuotojo būsena",
              "KET pažeidimas", "Mašinos firma","Dangos būklė",
              "Paros metas", "Oro salygos", "Kelio apšvietimas", "Mirtys")
    try:
        if to_excel:
            df.to_excel(f"Eismo_įvykiai({years_from_to}).xlsx", index=False)
        else:
            for year in unique_years:
                year_df = df[df['Metai'] == year]
                year_df.to_csv(f"Eismo_įvykiai_{year}.csv", index=False)
    except Exception as e:
        print(f"Error occurred: {e}")    


#plot car incidents and deaths over time
def plot_car_incidents_and_deaths_per_year(df, unique_years, years_from_to, to_png=False):
    car_accidents = df.groupby("year")["accident_id"].nunique().to_numpy()
    deaths = df.groupby(['year', 'accident_id'])['deaths'].sum().reset_index()
    deaths_by_year = deaths.groupby('year')['deaths'].sum().to_numpy()
    death_percentages = [round(deaths_by_year[i]/car_accidents[i]*100, 2) for i in range(len(unique_years))]
    
    cmap = plt.get_cmap('Paired')
    color = cmap(np.arange(len(unique_years)))
    plt.scatter(car_accidents, deaths_by_year, c=color)
    for i, year in enumerate(unique_years):
        plt.annotate(f"{year} mirštamumas ({death_percentages[i]}%)", xy=(car_accidents[i], deaths_by_year[i]), xytext=(car_accidents[i]-600, deaths_by_year[i]+2))
   
    plt.title(f"Eismo įyvkių bei mirčių kiekis per metus ({years_from_to}).")
    plt.ylabel("Mirčių kiekis")
    plt.xlabel("Avarijų kiekis")
    if to_png:
        plt.savefig("Graphs/Avarijų_ir_mirčių_grafikas.png")
    else:
        plt.show()
    
#Plots the percentages of females and males that were apart of a car crash
def plot_female_vs_male(df, years_from_to, to_png=False):
    counts = np.array([(df['driver_sex'] == 'Vyras').sum(), (df['driver_sex'] == 'Moteris').sum()])
    labels = ("Vyrai", "Moterys")
    sex_colors = ('#0099ff', '#ff99ff')
    plt.figure(figsize=(18,10))
    plt.pie(counts, labels=labels, autopct="%1.1f%%", colors=sex_colors)
    plt.title(f"Eismo dalyvių patekusių į avariją, pagal lytį, procentas ({years_from_to}).")
    
    if to_png:
        plt.savefig("Graphs/Moterų_ir_vyrų_grafikas.png")
    else:
        plt.show()
        
#Plots the most common combination of the 4 column values
def plot_environmental_reasons(df, years_from_to, to_png=False):
    unique_accidents = df.groupby("accident_id").first().reset_index()
    top_combinations = unique_accidents.groupby(["road_condition", "time_of_day", "weather_conditions", "road_lighting"]).size().nlargest(4)
    labels = [', '.join(map(str, tpl)) for tpl in top_combinations.index.tolist()]
    colors = {"#6929c4", "#012749", "#009d9a", "#ee538b"}
    
    plt.figure(figsize=(16, 10))
    plt.bar(labels, top_combinations.values, width=0.3, color=colors)
    plt.ylabel('Kiekis')
    plt.title(f"Aplinkinių salygų įtaka avarijomis. Labiausiai pasitaikančios kombinacijos ({years_from_to}).\n1. Kelio danga, 2. Dienos metas, 3. Oro salygos, 4. Kelio apšvietimas")
    
    if to_png:
        plt.savefig("Graphs/Aplinkinių_priežasčių_grafikas.png")
    else:
        plt.show()

#Plots variouse stats of drunk drivers
def plot_drunk_driver_data(df, unique_years, years_from_to, to_png=False):
    drunk_drivers = df.loc[(df["driver_state"] == "Neblaivus") | (df["driver_state"] == "Atsisakė būti patikrintas")]
    fig, axs = plt.subplots(2,2, figsize=(18, 10))
    
    drunk_drivers_by_year = drunk_drivers.groupby('year').size()
    
    top_5_cars = drunk_drivers['driver_car_firm'].drop(drunk_drivers[drunk_drivers['driver_car_firm'] == 'Nežinoma'].index).value_counts().head(5)
    car_colors = ("#002d9c", "#009d9a", "#9f1853", "#570408", "#a56eff")

    age_data = drunk_drivers.loc[drunk_drivers['driver_age'] != 'Nežinoma', 'driver_age'].tolist()
    
    drivers = len(df)
    counts = drunk_drivers.groupby('driver_sex').size()
    total_drunk_drivers = counts.sum()
    male_count = counts['Vyras']
    female_count = counts['Moteris']
    known_sex_count = male_count + female_count
    unknown_count = counts['Nežinoma'] #Some drunk drivers didnt have their sex logged
    sex_colors = ('#0099ff', '#ff99ff')
    
    ax1 = axs[0,0]
    ax1.plot(unique_years, drunk_drivers_by_year, marker="o")
    for x, y in zip(unique_years, drunk_drivers_by_year):
        ax1.text(x,y,y, ha="center", va="bottom")
    ax1.set_title("Girtų vairuotojų, patekusių į avariją, kiekis per metus.")
    ax1.set_ylabel("Kiekis")
    
    ax2 = axs[0,1]
    ax2.bar(top_5_cars.index, top_5_cars.values, width=0.5, color=car_colors)
    ax2.set_ylabel("Mašinų kiekis")
    ax2.set_title("5 dažniausiai naudojamos mašinų firmos.")
    
    ax3 = axs[1,0]
    ax3.boxplot(age_data, vert=False, showfliers=True, whis=1.5,
             showcaps=True, whiskerprops=dict(linestyle='-', linewidth=2, color='red'),
             boxprops=dict(linestyle='-', linewidth=2, color='red'),
             medianprops=dict(linestyle='-', linewidth=2, color='orange'),
             meanprops=dict(marker='o', markeredgecolor='black',
                            markerfacecolor='green'))
    ax3.set_title("Amžių pasiskirstymas tarp girtų vairuotojų.")
    ax3.set_xlabel("Amžius")
    
    ax4 = axs[1,1]
    ax4.bar(0, male_count, color=sex_colors[0], width=0.25, align='center', label="Vyrai")
    ax4.bar(0, female_count, bottom=male_count, color=sex_colors[1], width=0.25, align='center', label="Moterys")
    ax4.set_ylim([0, known_sex_count])
    ax4.set_xticks([0])
    ax4.set_xticklabels(['Lytis'])
    ax4.set_title(f"Iš {drivers} vairuotojų, {total_drunk_drivers} buvo girti. Tarp tų girtu, {unknown_count} neturėjo savo lyties registruotos.")
    
    fig.suptitle(f"Girtų vairuotojų, kurie pateko į avariją grafikai ({years_from_to}).")
    plt.tight_layout()
    
    if to_png:
        plt.savefig("Graphs/Girtų_vairuotojų_grafikas.png")
    else:
        plt.show()

#Table of all the rules broken with the counts to them
def plot_ket(df, years_from_to,to_png=False):
    
    ket_positive= df[df["driver_ket"] != "Nežinoma"]
    ket_counts = ket_positive["driver_ket"].value_counts()
    table_data = list(zip(ket_counts.index, ket_counts.values))
    plt.figure(figsize=(18,10))
    table = plt.table(cellText=table_data, colLabels=[f"Ket taisykliu pažeidimai ({years_from_to})", "Kiekis"], loc="center", cellLoc='center', colWidths=[0.6,0.1])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)
    plt.axis('off')
    
    if to_png:
        plt.savefig("Graphs/Ket_pažeidimų lentelė.png")
    else:
        plt.show()
    
#returns all the functions in a tuple list. First element is for user prompt indexing, third element is the parameters
def get_functions():
    df = return_cleaned_df() 
    unique_years = get_unique_years(df)
    years_from_to = get_years_from_to(unique_years)

    return [("1", plot_car_incidents_and_deaths_per_year, [df, unique_years, years_from_to]),
    ("2", plot_female_vs_male, [df, years_from_to]),
    ("3", plot_environmental_reasons, [df, years_from_to]),
    ("4", plot_drunk_driver_data, [df, unique_years, years_from_to]),
    ("5", plot_ket, [df, years_from_to]),
    ("7", df_writer, [df, unique_years, years_from_to])]
