import mediapipe as mp
import cv2

class FaceTracker:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        # Use refine_landmarks=True to get accurate eye/iris details
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_draw.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

    def process_frame(self, img):
        """
        Processes the image to find face landmarks.
        Returns:
            processed_img: Image with visual markers
            nose_point: (x, y) coordinates of the nose tip
            blink_distance: Pixel distance between upper and lower eyelid of left eye
        """
        img_h, img_w, _ = img.shape
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Performance optimization: mark image as not writeable to pass by reference
        rgb_img.flags.writeable = False
        results = self.face_mesh.process(rgb_img)
        rgb_img.flags.writeable = True
        
        nose_point = None
        blink_distance = None

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0]
            
            # 1. Extract Nose (Landmark 1) for Mouse Movement
            nose = face_landmarks.landmark[1]
            nose_point = (nose.x, nose.y)  # Keep as normalized (0.0 to 1.0)
            
            # Visual feedback for Nose
            nx, ny = int(nose.x * img_w), int(nose.y * img_h)
            cv2.circle(img, (nx, ny), 8, (0, 255, 0), cv2.FILLED)

            # 2. Extract Left Eye (Landmarks 159 top, 145 bottom) for Clicking
            left_eye_top = face_landmarks.landmark[159]
            left_eye_bottom = face_landmarks.landmark[145]
            
            ly_top = int(left_eye_top.y * img_h)
            ly_bottom = int(left_eye_bottom.y * img_h)
            lx_center = int(left_eye_top.x * img_w)

            # Visual feedback for Eye
            cv2.circle(img, (lx_center, ly_top), 3, (0, 255, 255), cv2.FILLED)
            cv2.circle(img, (lx_center, ly_bottom), 3, (0, 255, 255), cv2.FILLED)
            
            # Calculate distance in pixels
            blink_distance = ly_bottom - ly_top

        return img, nose_point, blink_distance
