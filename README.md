# ocr-project

Chemical Structure Recognition Tool (based on OSRA)

### Structure of the output folder

- `in` - folder with original image with recognized structures
  - `image.png`
- `out` - folder with computer-visualized results of recognition
  - `image.png`
- `report.txt` - text file with SMILEs for all recognized structures + some metrics for quality recognition
- `report.png` - bond length vs confidence estimate

### Contents of the `report.txt` file

Separated by `'\t'`, following information is written to the file:

1. File name
2. SMILE
3. Flag if result matches the metadata (if provided)
4. Average bond length
5. Confidence estimate (OSRA)
6. Number of unrecognized atoms
7. Number of spelling and superatom corrections
8. Number of atoms with wrong valencies
9. Several others obtained from JAR (to be done)
