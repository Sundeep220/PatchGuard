from app.services.terminal_service import TerminalService

"""
This test script demonstrates how to use the TerminalService to run Maven commands.
It executes 'mvn clean test' on a sample project and prints the output.
"""

# Run 'mvn clean test' on the vulnerable Spring Boot application
result = TerminalService.run_command(
    ["mvn", "clean", "test"],
    "sandbox/vulnerable-spring-app"
)
print(result["stdout"])
# If the Maven command failed, print the standard error
if result["return_code"] != 0:
    print(result["stderr"])