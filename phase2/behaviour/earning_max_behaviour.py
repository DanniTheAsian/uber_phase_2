from phase2.behaviour.driver_behaviour import DriverBehaviour

class EarningMaxBehaviour(DriverBehaviour):
    def __init__(self, min_ratio):
        self.min_ratio = min_ratio

    def decide(self, driver: "Driver", offer: "Offer", time: int) -> bool:

        travel_time = offer.estimated_travel_time
        
        if travel_time > 0:
            ratio = offer.estimated_reward / travel_time
        else:
            ratio =  int('inf')

        return ratio >= self.min_ratio


     
