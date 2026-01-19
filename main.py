import cv2

def main():
    # Open the default camera (device index 0)
    # Change the argument to 1 or higher if you have multiple cameras
    cap = cv2.VideoCapture(0)

    # Check if the webcam was opened successfully
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        exit()

    print("Webcam accessed successfully! Press 'q' to exit.")
    count = 0
    while True:
        # Read a frame from the webcam
        # ret (boolean) indicates if the frame was captured successfully
        # frame (numpy array) contains the image data
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        count += 1
        print(f"Frame {count} captured successfully.")
        # Optional: Perform operations on the frame here (e.g., face detection,
        # converting to grayscale, etc.)
        # Example: converting to grayscale
        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the frame in a window named 'Webcam Stream'
        cv2.imshow('Webcam Stream', frame)

        # Wait for a key press for 1 millisecond
        # If the 'q' key is pressed, break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print("Hello from license-plate-recognitor!")


if __name__ == "__main__":
    main()
