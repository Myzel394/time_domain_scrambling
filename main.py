import wave
import array
import random

SPLIT_PARTS = 5


def transpose_parts(parts: list[int]):
    parts_copy = parts.copy()

    parts[0] = parts_copy[2]
    parts[1] = parts_copy[0]
    parts[2] = parts_copy[4]
    parts[3] = parts_copy[3]
    parts[4] = parts_copy[1]


def main() -> None:
    # Type _raw_wavefile as wave_read
    with wave.open("./lasttime.wav") as _raw_wavefile:
        with wave.open("output.wav", mode="wb") as write_file:
            wave_file: wave.Wave_read = _raw_wavefile

            metadata = wave_file.getparams()
            first_frame = wave_file.readframes(1)
            raw_frames = wave_file.readframes(metadata.nframes)

            frames = array.array("h", raw_frames)

            write_file.setnchannels(1)
            write_file.setsampwidth(metadata.sampwidth)
            write_file.setframerate(metadata.framerate)


            # Iterate over seconds
            for i in range(0, int(metadata.nframes / 2), metadata.framerate):
                second = frames[i:i + metadata.framerate]

                # Split the second into parts
                second_part_duration = int(metadata.framerate / SPLIT_PARTS)

                parts = [
                    second[(j * second_part_duration):(j * second_part_duration) + second_part_duration]
                    for j in range(0, SPLIT_PARTS + 1 )
                ]

                #random.shuffle(parts)
                transpose_parts(parts)

                new_second = []

                for part in parts:
                    new_second.extend(part)

                write_file.writeframes(array.array("h", new_second).tobytes())


if __name__ == "__main__":
    main()
