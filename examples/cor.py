from typing import Optional


class Handler:
    """Base class for all handlers in the chain."""

    def __init__(self, next_handler: Optional["Handler"] = None):
        self.next_handler = next_handler  # Points to the next handler in the chain

    def handle(self, request: str) -> str:
        """Handles request or passes it to the next handler."""
        if self.next_handler:
            return self.next_handler.handle(request)
        return "No solution found"  # Default response if no handler processes it


# Concrete Handlers
class Level1Support(Handler):
    def handle(self, request: str) -> str:
        if request == "password reset":
            return "Handled by Level 1 Support"
        return super().handle(request)  # Pass to next handler


class Level2Support(Handler):
    def handle(self, request: str) -> str:
        if request == "technical issue":
            return "Handled by Level 2 Support"
        return super().handle(request)  # Pass to next handler


class Manager(Handler):
    def handle(self, request: str) -> str:
        if request == "refund request":
            return "Escalated to Manager"
        return super().handle(request)  # Pass to next handler


# Set up the chain
support_chain = Level1Support(Level2Support(Manager()))

# Example Usage
print(support_chain.handle("password reset"))  # ✅ Handled by Level 1 Support
print(support_chain.handle("technical issue"))  # ✅ Handled by Level 2 Support
print(support_chain.handle("refund request"))  # ✅ Escalated to Manager
print(support_chain.handle("unknown issue"))  # ❌ No solution found
