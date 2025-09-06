# On-Device Model Performance

Looking at the document, I can see there are sections titled "## On-Device Model Performance" and "### Local Model Capabilities", but "Local Model Capabilities" appears to be a subsection (###) rather than a same-level section (##) as "On-Device Model Performance".

Based on the structure, here is the content between "## On-Device Model Performance" and "### Local Model Capabilities":

So you can see the structure here. We're firing off Claude code sub agents and we're having our sub agents then fire off our nano agent server. So if we open up GPT5 nano, so this is a Claude code sub agent and all it does is it takes whatever prompt was passed in. It has access to a single tool - our MCP nano prompt nano agent tool - and then we just pass in whatever our parent gives us, whatever the primary agent gives us. So simple enough.