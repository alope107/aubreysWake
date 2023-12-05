#---------------------------------------------------------------------------------------------------------------------
# TARGET is the name of the output.
# BUILD is the directory where object files & intermediate files will be placed.
# LIBBUTANO is the main directory of butano library (https://github.com/GValiente/butano).
# PYTHON is the path to the python interpreter.
# SOURCES is a list of directories containing source code.
# INCLUDES is a list of directories containing extra header files.
# DATA is a list of directories containing binary data.
# GRAPHICS is a list of directories containing files to be processed by grit.
# AUDIO is a list of directories containing files to be processed by mmutil.
# DMGAUDIO is a list of directories containing files to be processed by mod2gbt and s3m2gbt.
# ROMTITLE is a uppercase ASCII, max 12 characters text string containing the output ROM title.
# ROMCODE is a uppercase ASCII, max 4 characters text string containing the output ROM code.
# USERFLAGS is a list of additional compiler flags:
#     Pass -flto to enable link-time optimization.
#     Pass -O0 or -Og to try to make debugging work.
# USERASFLAGS is a list of additional assembler flags.
# USERLDFLAGS is a list of additional linker flags:
#     Pass -flto=<number_of_cpu_cores> to enable parallel link-time optimization.
# USERLIBDIRS is a list of additional directories containing libraries.
#     Each libraries directory must contains include and lib subdirectories.
# USERLIBS is a list of additional libraries to link with the project.
# DEFAULTLIBS links standard system libraries when it is not empty.
# USERBUILD is a list of additional directories to remove when cleaning the project.
# EXTTOOL is an optional command executed before processing audio, graphics and code files.
#
# All directories are specified relative to the project directory where the makefile is found.
#---------------------------------------------------------------------------------------------------------------------

# TODO(auberon): Make relative paths more portable
TARGET      :=  $(notdir $(CURDIR))
BUILD       :=  build
LIBBUTANO   :=  ../../tools/butano/butano
PYTHON      :=  python
SOURCES     :=  src ../../tools/butano/common/src
INCLUDES    :=  include ../../tools/butano/common/include
DATA        :=
GRAPHICS    :=  graphics ../../tools/butano/common/graphics
AUDIO       :=  audio ../../tools/butano/common/audio
DMGAUDIO    :=  dmg_audio ../../tools/butano/common/dmg_audio
ROMTITLE    :=  AUBREYSWAKE
ROMCODE     :=  SBTP
USERFLAGS   :=  -flto
USERASFLAGS :=  
USERLDFLAGS :=  
USERLIBDIRS :=  
USERLIBS    :=  
DEFAULTLIBS :=  
USERBUILD   :=  
EXTTOOL     :=  
SCRIPTS     := scripts
#---------------------------------------------------------------------------------------------------------------------
# Export absolute butano path:
#---------------------------------------------------------------------------------------------------------------------
ifndef LIBBUTANOABS
	export LIBBUTANOABS	:=	$(realpath $(LIBBUTANO))
endif

#---------------------------------------------------------------------------------------------------------------------
# Include main makefile:
#---------------------------------------------------------------------------------------------------------------------
include $(LIBBUTANOABS)/butano.mak

#---------------------------------------------------------------------------------
# Override build target to inject our script
#---------------------------------------------------------------------------------
$(BUILD):
    # From original 
	@$(PYTHON) -B $(BN_TOOLS)/butano_assets_tool.py --grit="$(BN_GRIT)" --mmutil="$(BN_MMUTIL)" \
			--audio="$(AUDIO)" --dmg_audio="$(DMGAUDIO)" --graphics="$(GRAPHICS)" --build=$(BUILD)
	
    # Custom duration calculator
    # TODO(auberon): Figure out why this runs every time even if dependencies haven't changed 
	@$(PYTHON) -B $(SCRIPTS)/duration_metadata.py $(BUILD)/bn_sound_items_info.h audio $(BUILD)/sound_duration_metadata.h

    # From original 
	@$(MAKE) --no-print-directory -C $(BUILD) -f $(CURDIR)/Makefile
