class UserInput:
    def __init__(self, 
                 per_person_budget, 
                 trip_length, 
                 trip_timeslot, 
                 traveler_type, 
                 citizenship):
        self.per_person_budget = per_person_budget
        self.trip_length = trip_length  # in days
        self.trip_timeslot = trip_timeslot  # e.g., "July"
        self.traveler_type = traveler_type  # e.g., "solo", "family"
        self.citizenship = citizenship  # e.g., "South Korea"


class DestinationSelector:
    def __init__(self, alone, duo, group):
        self.alone = alone
        self.duo = duo
        self.group = group

    def total(self, trip_data, user_input):
        accessibility = self.accessibility_score(trip_data, user_input)
        affordability = self.affordability_score(trip_data, user_input)
        seasonality = self.score_season(trip_data['season_data'], user_input)
        compatibility = self.compatibility_score(trip_data['fit_data'], user_input)
        visa = self.visa_score(trip_data['visa_data'], user_input)
        safety = self.safety_score(trip_data['safety_data'])
        language = self.language_score(trip_data['language_data'])

        return accessibility + affordability + seasonality + compatibility + visa + safety + language

    # -----------------------
    # ACCESSIBILITY
    # -----------------------

    def accessibility_score(self, trip_data, user_input):
        travel_score = self.travel_time_score(trip_data['travel_time'], user_input.trip_length)
        layover_score = self.layover_amount(trip_data['layovers'])
        return travel_score + layover_score

    def travel_time_score(self, travel_time, trip_length_days):
        max_ratio = 0.25
        limit_time = trip_length_days * 24 * max_ratio
        if travel_time <= limit_time * 0.3: 
            return 1.0
        elif travel_time <= limit_time * 0.6: 
            return 0.5
        else: 
            return 0.1

    def layover_amount(self, layovers):
        if layovers == 0: 
            return 1.0
        elif layovers == 1:
            return 0.7
        else: 
            return 0.3

    # -----------------------
    # AFFORDABILITY
    # -----------------------

    def affordability_score(self, budget_data, user_input):
        daily_cost = budget_data['daily_cost']
        travel_cost = budget_data['travel_cost']
        per_person_budget = user_input.per_person_budget
        trip_length = user_input.trip_length

        total_cost = daily_cost * trip_length + travel_cost
        margin = per_person_budget - total_cost

        if margin >= per_person_budget * 0.2:
            return 1.0
        elif margin >= 0:
            return 0.5
        else:
            return 0.0

    # -----------------------
    # SEASONALITY
    # -----------------------

    def score_season(self, season_data, user_input):
        four_season_score = self.season_score(
            season_data['ideal_season'],
            season_data['bad_season'],
            user_input.trip_timeslot
        )
        festive_season_score = self.festive_score(
            season_data['festive_season'],
            user_input.trip_timeslot
        )
        return four_season_score + festive_season_score

    def season_score(self, ideal_season, bad_season, trip_timeslot):
        if trip_timeslot in ideal_season:
            return 1.0
        elif trip_timeslot in bad_season:
            return 0.1
        else:
            return 0.5

    def festive_score(self, festive_season, trip_timeslot):
        if trip_timeslot in festive_season: 
            return 0.5
        else:
            return 0.1

    # -----------------------
    # COMPATIBILITY
    # -----------------------

    def compatibility_score(self, fit_data, user_input):
        return self.type_score(fit_data['type_fit'], user_input.traveler_type)

    def type_score(self, type_fit, traveler_type):
        return 1.5 if type_fit == traveler_type else 0.0

    # -----------------------
    # VISA
    # -----------------------

    def visa_score(self, visa_data, user_input):
        required_nationalities = visa_data.get('requires_visa', [])
        if user_input.citizenship in required_nationalities:
            return 0.0
        else:
            return 1.0

    # -----------------------
    # SAFETY
    # -----------------------

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

    # -----------------------
    # LANGUAGE
    # -----------------------

    def language_score(self, language_data):
        speaks_english = language_data['speaks_english']
        has_tourist_support = language_data['has_tourist_support']

        if speaks_english:
            return 1.0
        elif has_tourist_support:
            return 0.7
        else:
            return 0.3
