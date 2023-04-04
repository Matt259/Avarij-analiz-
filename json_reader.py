import json

class JSONReader:
    
    def __init__(self, path, year):
        self.__path = path
        self.__year = year
        
    def get_json_data(self):
        try:
            with open(self.__path, 'r', encoding='utf-8', errors='ignore') as f:
                data = json.load(f)
                return data
        except UnicodeEncodeError:
            print("Unicode error: try running through terminal")
        except Exception as e:
            print("An exception of type {0} occurred: {1}".format(type(e).__name__, e))    
    
    #filters out valuable data related to crashes
    def filter_data(self):
        data = self.get_json_data()
        accidents = []
        for index, accident in enumerate(data):
            
            accident_id = index
            driver_age = ""
            driver_sex = ""
            driver_state = ""
            driver_ket = ""
            driver_car_firm = ""
            road_condition = accident["dangosBukle"]
            time_of_day = accident["parosMetas"]
            weather_conditions = accident["meteoSalygos"]
            road_lighting = accident["kelioApsvietimas"] 
            deaths = accident["zuvusiuSkaicius"] 
            
            for index_people in range(len(accident["eismoDalyviai"])):
                if accident["eismoDalyviai"][index_people]["kategorija"] == "Automobilio vairuotojas":
                    
                    current_driver_id = accident["eismoDalyviai"][index_people]["tpId"]
                    driver_age = accident["eismoDalyviai"][index_people]["amzius"] 
                    driver_sex = accident["eismoDalyviai"][index_people]["lytis"]
                    driver_state = accident["eismoDalyviai"][index_people]["busena"]
                    driver_ket = accident["eismoDalyviai"][index_people]["dalyvioKetPazeidimai"][0] if accident["eismoDalyviai"][index_people]["dalyvioKetPazeidimai"] else None

                    for index_car in range(len(accident["eismoTranspPreimone"])):
                        
                        #sometimes tp ID is null even tho there is one car within the transport list so assign by default
                        if len(accident["eismoTranspPreimone"]) == 1:   
                            driver_car_firm = accident["eismoTranspPreimone"][index_car]["marke"]
                            
                        elif accident["eismoTranspPreimone"][index_car]["tpId"] == current_driver_id:
                            driver_car_firm = accident["eismoTranspPreimone"][index_car]["marke"]
                            
                        filtered_accident = {
                        "year": self.__year,
                        "accident_id": accident_id,
                        "driver_age": driver_age,
                        "driver_sex": driver_sex,
                        "driver_state": driver_state,
                        "driver_ket": driver_ket,
                        "driver_car_firm": driver_car_firm,
                        "road_condition": road_condition,
                        "time_of_day": time_of_day,
                        "weather_conditions": weather_conditions,
                        "road_lighting": road_lighting,
                        "deaths": deaths}
                        accidents.append(filtered_accident)
                        break

        return accidents
    
