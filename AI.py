from datetime import datetime #, timedelta

class Flight:
    def __init__(self, flight_id, source, destination, departure_time, arrival_time, aircraft_id, cargo_id):
        self.flight_id = flight_id
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.aircraft_id = aircraft_id
        self.cargo_id = cargo_id

class Aircraft:
    def __init__(self, aircraft_id, capacity):
        self.aircraft_id = aircraft_id
        self.capacity = capacity
        self.schedule = []

class Cargo:
    def __init__(self, cargo_id, weight):
        self.cargo_id = cargo_id
        self.weight = weight
        self.flight_id = None

class Scheduler:
    def __init__(self):
        self.flights = []
        self.aircrafts = []
        self.cargos = []

    def add_flight(self, flight):
        self.flights.append(flight)

    def add_aircraft(self, aircraft):
        self.aircrafts.append(aircraft)

    def add_cargo(self, cargo):
        self.cargos.append(cargo)

    def schedule_flights(self):
        # Sort flights based on departure time
        self.flights.sort(key=lambda x: datetime.strptime(x.departure_time, "%H:%M"))

        for flight in self.flights:
            aircraft = self.find_available_aircraft(flight)
            if aircraft:
                aircraft.schedule.append(flight)
                flight.aircraft_id = aircraft.aircraft_id

    def allocate_cargo(self):
        # Sort cargos based on weight
        self.cargos.sort(key=lambda x: x.weight, reverse=True)

        for cargo in self.cargos:
            for aircraft in self.aircrafts:
                if aircraft.aircraft_id == cargo.flight_id:
                    if self.can_add_cargo(aircraft, cargo):
                        aircraft.schedule[-1].cargo_id = cargo.cargo_id
                        cargo.flight_id = aircraft.aircraft_id
                        break

    def find_available_aircraft(self, flight):
        for aircraft in self.aircrafts:
            if self.can_schedule_flight(aircraft, flight):
                return aircraft
        return None

    def can_schedule_flight(self, aircraft, flight):
        for scheduled_flight in aircraft.schedule:
            if self.is_flight_overlap(scheduled_flight, flight):
                return False
        return True

    def is_flight_overlap(self, flight1, flight2):
        departure1 = datetime.strptime(flight1.departure_time, "%H:%M")
        arrival1 = datetime.strptime(flight1.arrival_time, "%H:%M")
        departure2 = datetime.strptime(flight2.departure_time, "%H:%M")
        arrival2 = datetime.strptime(flight2.arrival_time, "%H:%M")

        return departure1 < arrival2 and departure2 < arrival1

    def can_add_cargo(self, aircraft, cargo):
        total_weight = sum(c.weight for c in aircraft.schedule[-1].cargo_id)
        return total_weight + cargo.weight <= aircraft.capacity

    def print_schedule(self):
        for aircraft in self.aircrafts:
            print("Aircraft ID:", aircraft.aircraft_id)
            for flight in aircraft.schedule:
                print("Flight ID:", flight.flight_id)
                print("Source:", flight.source)
                print("Destination:", flight.destination)
                print("Departure Time:", flight.departure_time)
                print("Arrival Time:", flight.arrival_time)
                print("Cargo ID:", flight.cargo_id)
                print("-----------------------------")

# Example usage
if __name__ == "__main__":
    # Create a scheduler
    scheduler = Scheduler()

    # Add flights
    flight1 = Flight("F1", "City A", "City B", "09:00", "11:00", "101","")
    flight2 = Flight("F2", "City B", "City C", "12:00", "14:00", "102","")
    flight3 = Flight("F3", "City A", "City C", "09:30", "12:00", "101","")
    scheduler.add_flight(flight1)
    scheduler.add_flight(flight2)
    scheduler.add_flight(flight3)

    # Add aircrafts
    aircraft1 = Aircraft("A1", 200)
    aircraft2 = Aircraft("A2", 150)
    scheduler.add_aircraft(aircraft1)
    scheduler.add_aircraft(aircraft2)

    # Add cargos
    cargo1 = Cargo("C1", 100)
    cargo2 = Cargo("C2", 50)
    scheduler.add_cargo(cargo1)
    scheduler.add_cargo(cargo2)

    # Schedule flights
    scheduler.schedule_flights()

    # Allocate cargos
    scheduler.allocate_cargo()

    # Print the schedule
    scheduler.print_schedule()

