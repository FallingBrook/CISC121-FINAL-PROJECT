# Linear Search
I chose the Linear Search algorithm because it is a foundational, stepping stone algorithm. This is the algorithm most programmers first learn because at its core it is a for loop, which is a necessary statement programmers must know. This means by learning Linear Search you not only unlock a powerful searching algorithm but also come to understand how a fundamental programming statement works. Furthermore, Linear Search is also a good first step toward understanding how search algorithms and time complexity work. The sequential examination Linear Search offers is present in a variety of topics making it a core building block for understanding complex techniques. 

## Demo video/gif/screenshot of test
https://drive.google.com/file/d/1JGnhNCAGlZL21Ni4f8tRm-CWZWQ-AjiR/view?usp=sharing

For testing and verification, I used both the preset lists and custom inputs:
- Best case: Target at index 0 (using the “Best Case” button).
- Worst case: Target at the last index (using the “Worst Case” button).
- Not found: Target not present in the list (using the “Not Found” button).
- Custom inputs: Lists with negative numbers, repeated values, and invalid input (e.g., non-integers or empty lists) to confirm that the app shows clear error messages.

## Problem Breakdown & Computational Thinking
### Decomposition
Create a function that takes a list and a target integer as a parameter, create a for loop that loops through the list, within the loop check if the current list element equals the target, if it does return True/index, after the for loop return False.
### Pattern Recognition
Linear Search repeatedly compares the values in the list to the target until it either finds the target or reaches the end of the list.
### Abstraction
The user should see each item in the list being compared to the target. I can show this by mapping a list to a grid and letting the user pick a number. I will show a pointer that starts at the beginning of the list and continues comparing each item until the index either reaches the target or the end of the list. I should also make sure we show the current index the pointer is at and some text that explains each new process as it happens. I plan to show example code but the actual loop structure will not be shown to the user. Additionally, the user will not be shown how the list is stored in memory and how each item is accessed. Lastly, if the user inputs an invalid list we will tell them there is an error but we do not show them the internal error handling logic.

### Algorithm Design
When the user runs the program they will be met with two tabs. The first tab includes text informing the user of the importance of linear search as a fundamental algorithm. They will be prompted to switch tabs once they have read all the information. The second tab is where the actual visualizer takes place. The user will be met with two input boxes and 5 different buttons. One input box will prompt the user for a list while the other prompts for the target. Three of the buttons automatically change the list and target to preset worst, best, and not found cases while the other two are start/reset and next step buttons. When a search is started, the list is displayed as a series of boxes with text underneath explaining each step of the process as the user steps through the algorithm. At the very bottom of the page, I plan to include example linear search code.

### Flowchart:
<img width="1292" height="1122" alt="CISC121-FINAL_PROJECT drawio" src="https://github.com/user-attachments/assets/31e9342e-ac15-4ddb-8adc-32452f2f7883" />

## Steps to Run
1. Download app.py and import it to your IDE
2. Install python 3
3. Install gradio (pip install gradio)
4. Run app.py
5. Open the link outputted in the console
## Hugging Face Link
https://huggingface.co/spaces/FallingBrook/CISC121-PROJECT-FINAL
## Author & Acknowledgment
All written explanations in this README are completely written by me.
The logic, structure, and overall design of this project was developed by me.
ChatGPT was used for the following: commenting, code polishing, and css assistance (because I have no experience with css).
I also used ChatGPT for debugging when I got runtime errors in hugging face. It guided me to create a requirements.txt file.
My approach to this project aligns with the allowed AI level guidelines.
