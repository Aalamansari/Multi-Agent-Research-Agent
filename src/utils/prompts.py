analyst_instructions =  """
You are tasked to create a set of AI analyst personas following the below instructions carefully:
1. First, review the research topic:
{topic}
2. Examine any enditorial feedback that has been optionally provided to guide creation of the analyst:
{human_analyst_feedback}
3. Determine the interesting themes based upon documents and / or feedback above.
4. Pick the top {max_analysts} theme.
5. Assign one analyst to each theme.
"""