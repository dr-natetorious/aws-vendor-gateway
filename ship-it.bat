@ECHO OFF
@ECHO ==================================
@ECHO Deployment Tool
@ECHO Nate Bachmeier - Amazon Solutions
@ECHO ==================================

@SETLOCAL enableextensions enabledelayedexpansion
@SET base_path=%~dp0
@PUSHD %base_path%

@CALL docker build -t vndrgtwy-deploy images/cdk-deploy
@CALL docker run -it -v %userprofile%\.aws:/root/.aws -v %cd%:/files -w /files vndrgtwy-deploy ship-it

@POPD