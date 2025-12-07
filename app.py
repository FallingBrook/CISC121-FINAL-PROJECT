import gradio as gr
import time

# Text used for the intro typewriter effect
INTRO_TEXTS = [
    "Welcome! This tool will walk you through how linear search works!",
    "Linear Search is often the first algorithm programmers learn. This is because it naturally introduces how loops and iteration work.",
    "What makes Linear Search important is its simplicity and versatility. It works on any list, in any order, and helps new programmers understand how loops operate.",
    "Studying Linear Search is a key step toward understanding more advanced search techniques and time complexity. Its sequential approach appears in many areas of computing, making it a fundamental building block for deeper learning.",
    "Click the app tab at the top to try out the visualizer!"
]

def typewriterWithState(index: int):
    """
    Simple typewriter animation that cycles through INTRO_TEXTS.
    Returns the progressively built string, the next index, and a counter label.
    """
    index = index % len(INTRO_TEXTS)
    text = INTRO_TEXTS[index]
    nextIndex = (index + 1) % len(INTRO_TEXTS)
    counter = f"{index + 1}/{len(INTRO_TEXTS)}"

    out = ""
    for ch in text:
        out += ch
        time.sleep(0.02)
        # Stream partial text, next index, and counter
        yield out, nextIndex, counter

# Linear search visualizer
def renderArray(arr, currentIndex=None, foundIndex=None):
    """
    Render the array as a row of boxes in HTML.
    Optionally highlight the current index and the found index.
    """
    boxes = []
    for i, v in enumerate(arr):
        classes = ["ls-box"]

        if foundIndex is not None and i == foundIndex:
            classes.append("ls-found")
        elif currentIndex is not None and i == currentIndex:
            classes.append("ls-current")

        boxes.append(
            f"""
            <div class="{' '.join(classes)}">
                <div class="ls-value">{v}</div>
                <div class="ls-index">i = {i}</div>
            </div>
            """
        )

    return f'<div class="ls-container">{"".join(boxes)}</div>'

def parseInputs(arrayText, targetText):
    """
    Convert the raw text inputs into a list of ints and an int target.
    Raises ValueError if the list is empty or parsing fails.
    """
    if not arrayText or not arrayText.strip():
        raise ValueError("List is empty.")

    parts = arrayText.replace(",", " ").split()
    arr = [int(p) for p in parts]
    target = int(targetText)
    return arr, target

def resetSearch(arrayText, targetText):
    """
    Initialize the linear search:
    - Parse inputs
    - Render the array with no highlights
    - Reset search state (index, found flag, step counter)
    """
    try:
        arr, target = parseInputs(arrayText, targetText)
    except Exception as e:
        html = f"<p style='color:red;'>Error: {e}</p>"
        status = "Could not start the search."
        explanation = "Check that the list and target are valid integers."
        # Return default state when initialization fails
        return html, status, explanation, 0, -1, True, "**Step:** 0", 0, arrayText, targetText

    index = 0
    foundIndex = -1
    isDone = False
    step = 0

    # No element highlighted on reset
    html = renderArray(arr, currentIndex=None, foundIndex=None)
    status = "Search ready. Nothing checked yet."
    explanation = (
        "Your list is shown above.\n\n"
        "Linear search will start at index 0 and move to the right.\n"
        "Click Next Step to check the first element."
    )
    stepText = f"**Step:** {step}"

    return html, status, explanation, index, foundIndex, isDone, stepText, step, arrayText, targetText

def nextStep(arrayText, targetText, index, foundIndex, isDone, step, lastArrayText, lastTargetText):
    """
    Perform a single step of linear search:
    - If already finished, just explain the result.
    - Otherwise, check the current index and either stop or move to the next.
    """
    try:
        arr, target = parseInputs(arrayText, targetText)
    except Exception as e:
        html = f"<p style='color:red;'>Error: {e}</p>"
        status = "Could not continue the search."
        explanation = "Fix the inputs and press **Start / Reset Search** again."
        return html, status, explanation, index, foundIndex, True, f"**Step:** {step}", step, lastArrayText, lastTargetText

    # If the user changed the list or target since last step, reset the search state
    if arrayText != lastArrayText or targetText != lastTargetText:
        index = 0
        foundIndex = -1
        isDone = False
        step = 0

    length = len(arr)

    # If search is already done, just keep showing the final result
    if isDone:
        html = renderArray(arr, currentIndex=None, foundIndex=None if foundIndex == -1 else foundIndex)
        if foundIndex != -1:
            status = f"Search finished. Target {target} was at index {foundIndex}."
            explanation = "We already found the target, so there are no more steps."
        else:
            status = f"Search finished. Target {target} is not in the list."
            explanation = "Every element was checked and none matched the target."
        return html, status, explanation, index, foundIndex, isDone, f"**Step:** {step}", step, arrayText, targetText

    # If we have gone past the last index, the target is not in the list
    if index >= length:
        html = renderArray(arr, currentIndex=None, foundIndex=None)
        status = f"Reached the end. Target {target} not found."
        explanation = "There are no more elements to check, so the target is not here."
        step += 1
        return html, status, explanation, index, foundIndex, True, f"**Step:** {step}", step, arrayText, targetText

    # Normal step: check the current index
    value = arr[index]
    html = renderArray(arr, currentIndex=index, foundIndex=None)

    if value == target:
        # Target found at this index
        html = renderArray(arr, currentIndex=None, foundIndex=index)
        status = f"Found {target} at index {index}."
        explanation = (
            f"At index {index}, the value {value} equals the target.\n"
            "In code, this is where the function would return this index."
        )
        foundIndex = index
        isDone = True
    else:
        # Not found here; move to next index
        status = f"Checking index {index}: {value} != {target}."
        explanation = (
            f"The value at index {index} is {value}, which does not match the target.\n"
            "We move on to the next index."
        )
        index += 1

    step += 1
    stepText = f"**Step:** {step}"

    return html, status, explanation, index, foundIndex, isDone, stepText, step, arrayText, targetText

# Example inputs
def loadBestCase():
    """Example where the target is at index 0."""
    return "5 9 12 7", "5"

def loadWorstCase():
    """Example where the target is at the last index."""
    return "2 4 6 8 10", "10"

def loadNotFoundCase():
    """Example where the target is not in the list."""
    return "1 3 5 7 9", "4"

cssStyles = """
<style>
.typewriter-text * {
    font-size: 25px !important;
    font-weight: 600 !important;
    text-align: center !important;
}

.generating {
    border: none !important;
}

.ls-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    margin-top: 20px;
}

.ls-box {
    width: 70px;
    height: 70px;
    border: 2px solid #ccc;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    font-family: monospace;
    background-color: #f9f9f9;
}

.ls-value {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 4px;
}

.ls-index {
    font-size: 12px;
    color: #666;
}

.ls-current {
    border-color: #facc15;
    box-shadow: 0 0 10px rgba(250, 204, 21, 0.7);
}

.ls-found {
    background-color: #bbf7d0;
    border-color: #22c55e;
    box-shadow: 0 0 10px rgba(34, 197, 94, 0.7);
}
</style>
"""

with gr.Blocks() as demo:
    # Inject CSS
    gr.HTML(cssStyles)

    with gr.Tabs(selected=1):
        # Intro tab with typewriter effect
        with gr.Tab("Intro", id=1):
            introState = gr.State(0)
            counterMarkdown = gr.Markdown("")
            introMarkdown = gr.Markdown("", elem_classes=["typewriter-text"])
            nextButton = gr.Button("Next")

            gr.Markdown(
                "When you're ready, click the App tab above to try the linear search visualizer."
            )

            nextButton.click(
                fn=typewriterWithState,
                inputs=introState,
                outputs=[introMarkdown, introState, counterMarkdown],
            )

            demo.load(
                fn=typewriterWithState,
                inputs=introState,
                outputs=[introMarkdown, introState, counterMarkdown],
            )

        # App tab with the linear search visualizer
        with gr.Tab("App", id=2):
            gr.Markdown("## Linear Search Visualizer")

            # Input row for list and target
            with gr.Row():
                arrayTextbox = gr.Textbox(
                    label="List (comma or space separated)",
                    value="2, 5, 8, 3, 9, 1",
                    placeholder="e.g. 2 5 8 3 9 1",
                )
                targetTextbox = gr.Textbox(
                    label="Target (integer)",
                    value="3",
                    placeholder="e.g. 3",
                )

            # Buttons to load example cases
            with gr.Row():
                bestCaseButton = gr.Button("Best Case")
                worstCaseButton = gr.Button("Worst Case")
                notFoundButton = gr.Button("Not Found")

            bestCaseButton.click(
                loadBestCase,
                inputs=None,
                outputs=[arrayTextbox, targetTextbox],
            )
            worstCaseButton.click(
                loadWorstCase,
                inputs=None,
                outputs=[arrayTextbox, targetTextbox],
            )
            notFoundButton.click(
                loadNotFoundCase,
                inputs=None,
                outputs=[arrayTextbox, targetTextbox],
            )

            # Control buttons
            startButton = gr.Button("Start / Reset Search")
            stepButton = gr.Button("Next Step")

            # Outputs: visualization, status, explanation, step number
            vizHtml = gr.HTML()
            statusMarkdown = gr.Markdown("Status will appear here.")
            explanationMarkdown = gr.Markdown("Explanation will appear here.")
            stepMarkdown = gr.Markdown("**Step:** 0")

            # Code example (now labeled)
            codeMarkdown = gr.Markdown(
                "### Example Code\n"
                "```python\n"
                "def linear_search(arr, target):\n"
                "    for i in range(len(arr)):\n"
                "        if arr[i] == target:\n"
                "            return i\n"
                "    return -1\n"
                "```"
            )

            # Internal state for the algorithm
            indexState = gr.State(0)
            foundState = gr.State(-1)
            doneState = gr.State(True)
            stepState = gr.State(0)
            lastArrayState = gr.State("")
            lastTargetState = gr.State("")

            # Reset / start the search
            startButton.click(
                fn=resetSearch,
                inputs=[arrayTextbox, targetTextbox],
                outputs=[
                    vizHtml,
                    statusMarkdown,
                    explanationMarkdown,
                    indexState,
                    foundState,
                    doneState,
                    stepMarkdown,
                    stepState,
                    lastArrayState,
                    lastTargetState,
                ],
            )

            # Perform a single step of the search
            stepButton.click(
                fn=nextStep,
                inputs=[arrayTextbox, targetTextbox, indexState, foundState, doneState, stepState, lastArrayState, lastTargetState],
                outputs=[vizHtml, statusMarkdown, explanationMarkdown, indexState, foundState, doneState, stepMarkdown, stepState, lastArrayState, lastTargetState,]
            )

# Start app
demo.launch()
