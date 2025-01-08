# Directory Synchronizer

This project is a Python-based directory synchronization tool that keeps two directories in sync by mirroring the contents of an **origin** directory into a **replica** directory at specified intervals. The tool monitors changes in the origin directory and applies them to the replica directory, including additions, deletions, and updates of files and directories.

## Features

- Synchronizes two directories with configurable time intervals.
- Handles file additions, deletions, and updates.
- Maintains a log of actions performed for auditing and debugging.
- Validates input parameters to ensure correctness.
- OS independendent implemetation

## Requirements

- Python 3.6 or higher
  
## Installation

1. Clone the repository:
   git clone <repository-url>
   cd <repository-directory>
