from neural1.models import FakeProvider
from neural1.scheduling import LogicalAgent, PopulationScheduler
from neural1.world import VirtualApple1World

world = VirtualApple1World()
agents = [LogicalAgent("A", "p"), LogicalAgent("B", "p")]
scheduler = PopulationScheduler(world, agents, {"p": FakeProvider(default="0300: 41")}, seed=7)
scheduler.round("DEPOSIT", lambda s: [s])
before = world.snapshot()
agents[0].reset_context()
print("Private lists distinct:", agents[0].private_context is not agents[1].private_context)
print("A context empty:", not agents[0].private_context)
print("RAM survived:", world.snapshot() == before)
assert not agents[0].private_context and world.snapshot() == before
