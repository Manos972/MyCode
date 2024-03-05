from pathlib import Path

dirs = {".pdf" : "Documents", ".PDF" : "Documents", ".txt" : "Documents", ".odp" : "Documents", ".xls" : "Documents",
	".csv" : "Documents", ".docx" : "Documents", ".pptx" : "Documents", ".png" : "Images", ".jpeg" : "Images",".dmg" : "Images",
	".jpg" : "Images", ".bmp" : "Images", ".mp4" : "Videos", ".avi" : "Videos", ".gif" : "Videos", ".zip" : "Archives",
	".mp3" : "Musiques", ".wav" : "Musiques", ".flac" : "Musiques", ".exe" : "Programme", ".msi" : "Programme",
	".json" : "Coding",".pem" : "Coding", ".py" : "Coding"}

tri_dir = Path.home() / "Downloads"

files = [f for f in tri_dir.iterdir() if f.is_file()]

for f in files :
	output_dir = tri_dir / dirs.get(f.suffix, "Autres")
	output_dir.mkdir(exist_ok=True)
	f.rename(output_dir / f.name)
