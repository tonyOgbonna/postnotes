Update the application with the following enhancements:
1. Keep track of processed Video url / Processing Style pair, and not process them again
2. Append the name of the used System Instruction at the end of the output filename. The name is gotten from the Level 1 header (#) detail inside the System Instruction file on the first line.
3. Include the following Obsidian style Frontmatter Schema at the beginning of the output file:
Frontmatter Schema
"
---
Title: "Original Video Title"
link: "Video URL"
channel: "Channel Name"
processed_at: 2025-03-09T01:20:00+01:00
llm_model: "claude-3-opus-20240229"
system_instruction: "summary_enhanced.md"
tags: ["summary_enhanced"]
---
"
4. The output file final name should be created from the first Level 1 header (#) detail of the LLM output designated with '# Title:", with the name of the used System Instruction appended at the end
5. The frontmatter tags entry should be created from the System Instruction name.

Implement each feature one after the other and move on to the next only after the current one is tested and working ok.