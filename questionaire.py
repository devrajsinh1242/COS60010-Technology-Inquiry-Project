import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display (1024x768 screen)
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Math Level Quiz")

# Load the background image and scale it to fit the screen
background_image = pygame.image.load("background_ball.jpg")  # Make sure the image file is in the same directory
background_image = pygame.transform.scale(background_image, (1024, 768))  # Scale the image to fit the screen

# Set up fonts and colors
font = pygame.font.SysFont(None, 55)
small_font = pygame.font.SysFont(None, 35)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load sounds for correct and wrong answers
correct_answer_sound = pygame.mixer.Sound("right_answer.mp3")
wrong_answer_sound = pygame.mixer.Sound("wrong_answer.mp3")

# Map for operator to operation names
operator_names = {
    '+': 'Addition',
    '-': 'Subtraction',
    '*': 'Multiplication',
    '/': 'Division'
}


# Function to generate math question with non-negative subtraction
def generate_question(operator):
    num1 = random.randint(1, 99)  # One- or two-digit numbers (1-99)
    num2 = random.randint(1, 99)  # One- or two-digit numbers (1-99)

    if operator == '+':
        correct_answer = num1 + num2
        question = f"{num1} + {num2} = ?"
    elif operator == '-':
        # Ensure non-negative results for subtraction
        if num1 < num2:
            num1, num2 = num2, num1
        correct_answer = num1 - num2
        question = f"{num1} - {num2} = ?"
    elif operator == '*':
        correct_answer = num1 * num2
        question = f"{num1} * {num2} = ?"
    elif operator == '/':
        while num2 == 0 or num1 % num2 != 0:  # Ensure divisibility for integer results
            num1 = random.randint(1, 99)
            num2 = random.randint(1, 99)
        correct_answer = num1 // num2
        question = f"{num1} / {num2} = ?"
    return question, correct_answer


# Function to display text on the screen
def display_text(text, x, y, font, color=BLACK):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))


# Function to draw a button
def draw_button(text, x, y, width, height, color, font):
    pygame.draw.rect(screen, color, (x, y, width, height))
    display_text(text, x + 10, y + 10, font, WHITE)


# Function to determine the user's math level based on their score
def get_math_level(score):
    if score >= 16:
        return 4
    elif score >= 11:
        return 3
    elif score >= 6:
        return 2
    else:
        return 1


# Main game loop
def run_quiz():
    operators = ['+', '-', '*', '/']
    total_questions = 20
    questions_per_operator = 5  # 5 questions per operation
    score = 0
    input_answer = ''
    correct_answer = None
    input_box = pygame.Rect(340, 400, 400, 50)  # Text box for input
    submit_button = pygame.Rect(465, 600, 150, 50)  # Submit button in the middle for each question
    leave_button = pygame.Rect(465, 650, 150, 50)  # Leave Now button on the final page
    color_active = pygame.Color('lightskyblue3')
    color_inactive = pygame.Color('dodgerblue2')
    active = False
    color = color_inactive
    cursor_visible = True
    cursor_timer = 0
    cursor_blink_speed = 5000  # Blink every 5000 milliseconds (5 seconds)

    # Tracking correct answers for each operator
    correct_per_operator = {'+': 0, '-': 0, '*': 0, '/': 0}
    total_per_operator = {'+': 0, '-': 0, '*': 0, '/': 0}
    question_counts = {'+': 0, '-': 0, '*': 0, '/': 0}  # Track the number of questions per operator

    operator_queue = operators * questions_per_operator  # 5 questions for each operator
    question_count = 0  # Track total questions asked

    # Main loop
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Blit the background image

        if question_count < total_questions:
            if not correct_answer:  # Generate new question if needed
                operator = operator_queue[question_count]
                question, correct_answer = generate_question(operator)
                question_counts[operator] += 1

            # Display the question and score
            display_text(question, 340, 200, font)  # Adjusted position for the question
            display_text(f"Score: {score}", 340, 300, small_font)  # Adjusted position for the score

            # Show how many questions are completed and remaining
            display_text(f"Question {question_count + 1} of {total_questions}", 340, 500, small_font)
            display_text(f"{total_questions - question_count - 1} remaining", 340, 550, small_font)

            # Render the input box with cursor blink and highlight when active
            pygame.draw.rect(screen, color, input_box, 2)  # Draw the text box
            text_surface = font.render(input_answer, True, BLACK)
            screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))

            # Handle cursor blink and show it in the box
            if active:
                cursor_timer += pygame.time.get_ticks()
                if cursor_timer >= cursor_blink_speed:
                    cursor_visible = not cursor_visible  # Toggle visibility
                    cursor_timer = 0  # Reset timer

                if cursor_visible:
                    # Draw the cursor at the end of the input text
                    cursor_x = input_box.x + 10 + text_surface.get_width() + 2
                    cursor_y = input_box.y + 10
                    pygame.draw.rect(screen, BLACK, (cursor_x, cursor_y, 2, text_surface.get_height()))

            # Draw the "Submit" button
            draw_button("Submit", submit_button.x, submit_button.y, submit_button.width, submit_button.height, BLUE,
                        small_font)

        else:
            # Show final score and levels
            display_text(f"Your final score is: {score}/20", 340, 200, font)

            # Determine and display the user's math level
            math_level = get_math_level(score)
            display_text(f"You are Level {math_level}", 340, 250, font)

            # Display correction rates for each operation
            for op in operators:
                if total_per_operator[op] > 0:
                    correction_rate = (correct_per_operator[op] / total_per_operator[op]) * 100
                    operation_name = operator_names[op]  # Use the descriptive names
                    display_text(
                        f"{operation_name} Correction rate: {correction_rate:.2f}% ({correct_per_operator[op]}/{total_per_operator[op]})",
                        340, 300 + operators.index(op) * 50, small_font)

            # Draw the "Leave Now" button on the final page
            draw_button("Leave Now", leave_button.x, leave_button.y, leave_button.width, leave_button.height, RED,
                        small_font)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked inside the input box
                if input_box.collidepoint(event.pos):
                    active = True
                    color = color_active  # Highlight the box
                    cursor_visible = True  # Show cursor immediately when clicked
                else:
                    active = False
                    color = color_inactive  # Reset to inactive color

                # Check if "Submit" is clicked
                if submit_button.collidepoint(event.pos) and question_count < total_questions:
                    if input_answer:
                        total_per_operator[operator] += 1  # Track total attempts per operator
                        if int(input_answer) == correct_answer:
                            score += 1
                            correct_per_operator[operator] += 1  # Track correct answers
                            correct_answer_sound.play()  # Play sound for correct answer
                        else:
                            wrong_answer_sound.play()  # Play sound for wrong answer
                        question_count += 1
                        input_answer = ''  # Reset input for the next question
                        correct_answer = None  # Prepare for the next question

                # Check if "Leave Now" is clicked on the final page
                if leave_button.collidepoint(event.pos) and question_count >= total_questions:
                    running = False  # Exit the game

            elif event.type == pygame.KEYDOWN:
                if active:  # Input text only if the text box is active
                    if event.key == pygame.K_BACKSPACE:
                        input_answer = input_answer[:-1]  # Remove last digit
                    elif event.unicode.isdigit():
                        input_answer += event.unicode  # Collect digits for the answer

        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()


# Start the quiz
run_quiz()
