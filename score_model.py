class DestinationSelector:
    def __init__(self, alone, duo, group):
        self.alone = alone
        self.duo = duo
        self.group = group

    def total(self, trip_data):
        accessibility = self.accessibility_score(trip_data)
        affordability = self.affordability_score(trip_data)
        seasonality = seasonality_score(trip_data)
        compatibility = compatibility_score(trip_data)
        visa = visa_score(trip_data)
        safety = safety_score(trip_data)
        language = language_score(trip_data)

        return accessibility + affordability + seasonality + compatibility + visa + safety + language

    def accessability_score(self, trip_data):
        travel_score = self.travel_time_score(trip_data['travel_time'], trip_data['trip_length_days'])
        layover_score = self.layover_amount(trip_data['layovers'])
        return travel_score + layover_score

    def travel_time_score(self, travel_time, trip_length_days): # we will presume travel length above the 25% threshold is eliminated
        max = 0.25 # this number is set to ratio of 25%
        limit_time = trip_length_days * 24 * max # this will show the maximum hours user will use for travel time
        if travel_time <= limit_time * 0.3: 
            return 1.0
        elif travel_time <= limit_time * 0.6: 
            return 0.5
        else: 
            return 0.1

    def layover_amount(self, layovers):
        if layovers == 0: 
            return 1.0 # no layover is best
        elif layovers == 1:
            return 0.7
        else: 
            return 0.3
        
    def affordability_score(self, budget_data):
        daily_cost = budget_data['daily_cost']
        trip_length = budget_data['trip_length']
        travel_cost = budget_data['travel_cost']
        per_person_budget = budget_data['per_person_budget']

        total_cost = daily_cost * trip_length + travel_cost
        budget_margin = per_person_budget - total_cost # margin will help us calculate how tight we need to spend our budget for the trip

        if budget_margin >= per_person_budget * 0.2:
            return 1.0
        elif budget_margin >= 0:
            return 0.5
        else:
            return 0.0
        
    def seasonality_score(self, season_data):
        four_season_score = self.season_score(season_data['ideal_season'], season_data['bad_season'], season_data['trip_timeslot'])
        festive_season_score = self.festive_score(season_data['festive_season'], season_data['trip_timeslot'])
        return four_season_score + festive_season_score
    
    def season_score(self, ideal_season, bad_season, trip_timeslot):
        if trip_timeslot in ideal_season:
            return 1.0
        elif trip_timeslot in bad_season:
            return 0.1
        else:
            return 0.5
    
    def festive_score(self, festive_season, trip_time_slot):
        if trip_time_slot in festive_season: 
            return 0.5
        else:
            return 0.1
        
    def compatibility_score(self, fit_data):
        #travel_number_score = self.number_score(fit_data['number_fit'], fit_data['travler_number']) # shouldn't I change number of travlers itself into user_input class?
        travel_type_score = self.type_score(fit_data['type_fit'], fit_data['travler_type'])
        return travel_type_score # + travel_number_score
    
    def type_score(self, type_fit, travler_type):
        if type_fit == travler_type:
            return 1.5
        else:
            return 0
        
    def safety_score(self, safety_data):
        crime_index = safety_data['crime_index']
        political_stable = safety_data['political_stable']
        has_health_alert = safety_data['has_health_alert']

        if crime_index > 60 or not political_stable or has_health_alert:
            return 0.0
        elif crime_index > 40:
            return 0.5
        else:
            return 1.0

    def language_score(self, language_data):
        speaks_english = language_data['speaks_english']
        has_tourist_support = language_data['has_tourist_support']

        if speaks_english:
            return 1.0
        elif has_tourist_support:
            return 0.7
        else:
            return 0.3