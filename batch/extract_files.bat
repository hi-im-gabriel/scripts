@echo off

for /f %%a in ('dir /b') do (
	cd %%a\ && move "*.*" ".." && cd .. && rmdir %%a
)
