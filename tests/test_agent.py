from agents import Agent, Runner
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

"""
This test file demonstrates how to initialize and run a simple agent.
It's a basic example to verify the agent setup.
"""

agent = Agent(
    name="PatchPilot",
    instructions="You are a dependency remediation agent.",
    model="gpt-4o-mini",
)
# Run the agent with a simple prompt and print its final output
result = Runner.run_sync(
    agent,
    "Explain what dependency vulnerabilities are."
)

print(result.final_output)