import cv2
from pyzbar.pyzbar import decode

def read_qr_code():
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to capture image")
            break
        
        decoded_objects = decode(frame)
        
        for obj in decoded_objects:
            print("Data:", obj.data.decode('utf-8'))
            cv2.putText(frame, str(obj.data.decode('utf-8')), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        cv2.imshow("QR Code Scanner", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Scan the QR code with your webcam.")
    read_qr_code()
