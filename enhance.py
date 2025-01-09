import noisereduce as nr
from scipy.io import wavfile
import io

def purewave_enhance(audio_path):
    # Load the audio file
    try:
        rate, data = wavfile.read(audio_path)
    except FileNotFoundError:
        print("Error: The file was not found. Please make sure the file is in the correct location or use a different file name.")
        exit()
    
    # Perform noise reduction
    try:
        reduced_noise = nr.reduce_noise(y=data, sr=rate)
    except Exception as e:
        print(f"An error occurred during noise reduction: {e}")
        exit()

    try:
        # Write the denoised audio to a BytesIO stream
        buffer = io.BytesIO()
        wavfile.write(buffer, rate, reduced_noise)
        buffer.seek(0)  # Reset buffer position for reading
        return buffer
    except Exception as e:
        return {"error": f"An error occurred while preparing the audio response: {e}"}, 500


    # # Save the denoised audio
    # try:
    #     wavfile.write(output_path, rate, reduced_noise)
    # except Exception as e:
    #     print(f"An error occurred while writing the denoised audio: {e}")
    #     exit()

    # print("Audio denoising complete and saved in " + output_path)

