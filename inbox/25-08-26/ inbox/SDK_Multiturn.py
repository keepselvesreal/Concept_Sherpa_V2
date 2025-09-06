import asyncio
from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions, query

# Method 1: Using ClaudeSDKClient for persistent conversations
async def multi_turn_conversation():
    async with ClaudeSDKClient() as client:
        # First query
        await client.query("Let's refactor the payment module")
        async for msg in client.receive_response():
            # Process first response
            pass
        
        # Continue in same session
        await client.query("Now add comprehensive error handling")
        async for msg in client.receive_response():
            # Process continuation
            pass
        
        # The conversation context is maintained throughout

# Method 2: Using query function with session management
async def resume_session():
    # Continue most recent conversation
    async for message in query(
        prompt="Now refactor this for better performance",
        options=ClaudeCodeOptions(continue_conversation=True)
    ):
        if type(message).__name__ == "ResultMessage":
            print(message.result)

    # Resume specific session
    async for message in query(
        prompt="Update the tests", 
        options=ClaudeCodeOptions(
            resume="550e8400-e29b-41d4-a716-446655440000",
            max_turns=3
        )
    ):
        if type(message).__name__ == "ResultMessage":
            print(message.result)

# Run the examples
asyncio.run(multi_turn_conversation())