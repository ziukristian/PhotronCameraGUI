/*
 *	PDCSTR.h
 *	Photron Device Control SDK
 *	Structure Definition
 *
 *	Copyright (C) 2006-2012 PHOTRON LIMITED
 */

#include	"PDCVALUE.h"

#define SDK_RENEWAL

#ifdef SDK_RENEWAL
 //#if not defined(WIN32_LEAN_AND_MEAN)
 //#define WIN32_LEAN_AND_MEAN      // Exclude rarely-used stuff from Windows headers
 //#endif
 //#include <windows.h>
#else
#include	<vfw.h>
#endif
#ifndef	_PDC_STR_H_
#define	_PDC_STR_H_

#pragma	pack(4)
/*
 *	Device detect structure
 */
typedef struct {
	/*	Device code	*/
	unsigned long	m_nDeviceCode;
	/*	Virtual device number(IP-address)	*/
	unsigned long	m_nTmpDeviceNo;
	/*	Interface code	*/
	unsigned long	m_nInterfaceCode;
} PDC_DETECT_INFO, *PPDC_DETECT_INFO;

/*
 *	Device detect integration structure
 */
typedef struct {
	/*	Detected device num	*/
	unsigned long	m_nDeviceNum;
	/*	Device detect structure	*/
	PDC_DETECT_INFO	m_DetectInfo[PDC_MAX_DEVICE];
} PDC_DETECT_NUM_INFO, *PPDC_DETECT_NUM_INFO;

/*
 *	Frame information
 */
typedef struct {
	long			m_nStart;	/*	Recording start frame number	*/
	long			m_nEnd;		/*	Recording end frame number	*/
	long			m_nTrigger;	/*	Trigger frame number	*/
	long			m_nTwoStageLowToHigh;	/*	Twostage LOW->HIGH frame number	*/
	long			m_nTwoStageHighToLow;	/*	Twostage HIGH->LOW frame number	*/
	unsigned long	m_nTwoStageTiming;		/*	Twostage LOW->HIGH timming	*/
	long			m_nEvent[10];		/*	Event frame number	*/
	unsigned long	m_nEventCount;		/*	Event frame count	*/
	unsigned long	m_nRecordedFrames;		/*	Recording frame quantity	*/
} PDC_FRAME_INFO, *PPDC_FRAME_INFO;

/*
 *	Image data information
 */
typedef struct {
	long			m_nWidth;
	long			m_nHeight;
	long			m_nBytePerLine;
	unsigned short	m_nRealBitPerPixel;
	long			m_nInterleave;	/* Buffer Interleave	*/
} PDC_IMAGE_BUFF_INFO, *PPDC_IMAGE_BUFF_INFO;

/*	Bayer Convert Information	*/
typedef struct {
	unsigned long	m_nMode;
	unsigned long	m_nDeviceCode;
	void*			m_pLUTR;
	void*			m_pLUTG;
	void*			m_pLUTB;
	unsigned long	m_nOutputInterleave;
	unsigned long	m_nEdgeEnhance;
	unsigned long	m_nColorTempR;
	unsigned long	m_nColorTempG;
	unsigned long	m_nColorTempB;
	long			m_nColorMatrixRR;
	long			m_nColorMatrixRG;
	long			m_nColorMatrixRB;
	long			m_nColorMatrixGR;
	long			m_nColorMatrixGG;
	long			m_nColorMatrixGB;
	long			m_nColorMatrixBR;
	long			m_nColorMatrixBG;
	long			m_nColorMatrixBB;
} PDC_BAYER_CONVERT_INFO, *PPDC_BAYER_CONVERT_INFO;

/*
 *	IRIG information
 */
typedef struct {
	unsigned long	m_nDayOfYear;	//	Day
	unsigned char	m_nHour;		//	Hour
	unsigned char	m_nMinute;		//	Minute
	unsigned char	m_nSecond;		//	Second
	unsigned long	m_nMicroSecond;	//	Micro second
	unsigned char	m_ExistSignal;	//	Presence of signal
	unsigned long	m_Reserve;		//	Reserved
} PDC_IRIG_INFO, *PPDC_IRIG_INFO;

/*
 *	MCDL information
 */
typedef struct {
	unsigned char	m_nDigital[10];	/*	Digital	*/
	double			m_nAnalogA[10];	/*	AnalogA	*/
	double			m_nAnalogB[10];	/*	AnalogB	*/
	double			m_nAnalogC[10];	/*	AnalogC	*/
	double			m_nAnalogD[10];	/*	AnalogD	*/
} PDC_MCDL_INFO, *PPDC_MCDL_INFO;

/*
 *	IRIG / MCDL information
 */
typedef struct {
	PDC_IRIG_INFO	m_IRIGInfo;	/*	IRIG	*/
	PDC_MCDL_INFO	m_MCDLInfo;	/*	MCDL	*/
} PDC_IRIGMCDL_INFO, *PPDC_IRIGMCDL_INFO;

/*
*	ADC information
*/
typedef struct {
	float			m_nAnalog1[10];	/*	Analog1	*/
	float			m_nAnalog2[10];	/*	Analog2	*/
} PDC_ADC_INFO, *PPDC_ADC_INFO;


/*
*	Auto Exposure information
*/
typedef struct {
	unsigned long	m_nShutter;
} PDC_AUTO_EXPOSURE_INFO, *PPDC_AUTO_EXPOSURE_INFO;

/*
*	Temperature type1
*/
typedef struct{
	double m_nTemperatureCPU;/*CPU*/
	double m_nTemperatureSEN;/*SEN*/
	double m_nTemperatureMEM;/*Memory*/
	double m_nTemperatureFPGA;/*FPGA*/
}PDC_TEMPERATURE_DATA_TYPE1, *PPDC_TEMPERATURE_DATA_TYPE1;

/*
*	Temperature type2
*/
typedef struct{
    char m_nTemperatureCPU;/*CPU*/
    char m_nTemperatureSEN;/*SEN*/
    char m_nTemperatureFan;/*Fan*/             
}PDC_TEMPERATURE_DATA_TYPE2, *PPDC_TEMPERATURE_DATA_TYPE2;

/*
*	Temperature type3
*/
typedef struct{
    char m_nTemperatureSEN;/*SEN*/
    char m_nTemperatureFPGA;/*FPGA*/
    char m_nTemperatureMain;/*Main*/
    char m_nTemperatureHead;/*Head*/
}PDC_TEMPERATURE_DATA_TYPE3, *PPDC_TEMPERATURE_DATA_TYPE3;

/*
*	Temperature type4
*/
typedef struct{
	double m_nTemperatureCPU;/*CPU*/
	double m_nTemperatureSEN;/*SEN*/
	double m_nTemperatureMEM;/*Memory*/
	double m_nTemperatureFPGA;/*FPGA*/
	double m_nTemperatureMSP;/*MSP*/
}PDC_TEMPERATURE_DATA_TYPE4, *PPDC_TEMPERATURE_DATA_TYPE4;

/*
*	Temperature type5
*/
typedef struct {
	char m_nTemperatureCPU;          /*CPU FPGA*/
	char m_nTemperatureSEN;          /*SEN Board*/
	char m_nTemperatureFan;          /*Fan Board*/
	char m_nTemperatureCPUBoard;     /*CPU Board*/
	char m_nTemperatureSENSubBoard;  /*SEN Sub Board*/
	char m_nTemperatureTGMaster;     /*TG Master = SEN FPGA*/
}PDC_TEMPERATURE_DATA_TYPE5, * PPDC_TEMPERATURE_DATA_TYPE5;

/*
* Acceleration Data
*/
typedef struct {
	float m_fAccelerationX;
	float m_fAccelerationY;
	float m_fAccelerationZ;
}PDC_ACCELERATION_DATA, *PPDC_ACCELERATION_DATA;

/*
 *	Pre-LUT information
 */
typedef struct {
	long			m_nBrightnessR;
	long			m_nBrightnessG;
	long			m_nBrightnessB;
	long			m_nContrastR;
	long			m_nContrastG;
	long			m_nContrastB;
	double			m_nGainR;
	double			m_nGainG;
	double			m_nGainB;
	double			m_nGammaR;
	double			m_nGammaG;
	double			m_nGammaB;
	unsigned char	m_nPosiNegaR;
	unsigned char	m_nPosiNegaG;
	unsigned char	m_nPosiNegaB;
	unsigned char	m_nFreeMode;
} PDC_LUT_PARAMS, *PPDC_LUT_PARAMS;

/*
 *	AVI Frame Parameter
 */
typedef struct {
	long			m_nStart;
	long			m_nEnd;
	long			m_nTotal;
	long			m_nArea_start;
	long			m_nArea_end;
	long			m_nArea_total;
	long			m_nCurrent;
	long			m_nTrigger;
	long			m_nKey;
} PDC_AVI_FRAME_PARAMS, *PPDC_AVI_FRAME_PARAMS;

/*
 *	drop Frame List
 */
typedef struct pdc_drop_frame_list
{
  long			m_nFrame;		/* drop start frame number */
  unsigned long	m_nDropFrame;	/* number of dropped frame */
} PDC_DROP_FRAME_LIST, *PPDC_DROP_FRAME_LIST;

/* 
 * Original Image data Information
 */
typedef struct {
	unsigned long	m_nDeviceCode;
	unsigned long	m_nColorType;
	unsigned short	m_nBitDepth;
	unsigned long	m_nEffectiveBits;
	unsigned long	m_n8BitSel;
} PDC_ORG_IMAGE_INFO, *PPDC_ORG_IMAGE_INFO;

/*
 * Frame information
 */
typedef struct {
	long			m_nTrigger[1024];	/*	Trigger frame number	*/
	unsigned long	m_nTriggerCount;	/*	Trigger frame count		*/
} PDC_TRIGGER_FRAME_LIST, *PPDC_TRIGGER_FRAME_LIST;

/*
 * Save Frame Information
 */
typedef struct {
	long  nStartFrame;
	long  nEndFrame;
	long  nSkipFrame;  /*Number of Frame skip, when random skip set to -1*/
	long* pFrames;	 /*SetFrame Numbers when random skip, other Set to NULL*/
	unsigned long nFrameCount;

}PDC_SAVE_FRAME_INFO, *PPDC_SAVE_FRAME_INFO;

/*
* WiFi Information (WideChar)
*/
typedef struct {
	wchar_t strMacAddress[PDC_MAX_STRING_LENGTH];
	wchar_t strSSID[PDC_MAX_STRING_LENGTH];
	int nSignal;
	int nFrequency;
	wchar_t strPassword[32];
	int bConnected;
	int nLastSeenTimestamp;
} PDC_WIFI_INFOW, *PPDC_WIFI_INFOW;

/*
* WiFi Information (Multibyte)
*/
typedef struct {
	char strMacAddress[PDC_MAX_STRING_LENGTH];
	char strSSID[PDC_MAX_STRING_LENGTH];
	int nSignal;
	int nFrequency;
	char strPassword[32];
	int bConnected;
	int nLastSeenTimestamp;
} PDC_WIFI_INFOA, *PPDC_WIFI_INFOA;

#ifdef UNICODE
#define PDC_WIFI_INFO	PDC_WIFI_INFOW
#define PPDC_WIFI_INFO	PPDC_WIFI_INFOW
#else
#define PDC_WIFI_INFO	PDC_WIFI_INFOA
#define PPDC_WIFI_INFO	PPDC_WIFI_INFOA
#endif // !UNICODE

/*
* Storage Information
*/
typedef struct {
	__int64 nTotalSize;
	__int64 nAvailable;
	unsigned long nNumOfFiles;

} PDC_MEDIA_INFO, *PPDC_MEDIA_INFO;

/*
* Battery Information
*/
typedef struct {
	unsigned long	nVoltage; // mV
	unsigned long	nCharge;
	double			nTemperature;
	unsigned long	nElectricCurrent; // mA
	int			bPowerConnected;
	int			bBatteryCharging;
} PDC_BATTERY_INFO, *PPDC_BATTERY_INFO;

/*
* Record Info for FAST Drive and SD Card
*/
typedef struct {
	unsigned short	m_nInfoVersion;
	unsigned short	m_nSysVersion;
	unsigned long	m_nDate;
	unsigned long	m_nTime;
	unsigned long	m_nCameraType;
	unsigned short	m_nHeadType;
	unsigned short	m_nHeadNo;
	unsigned short	m_nMaxHeadNum;
	char			m_DeviceName[PDC_MAX_STRING_LENGTH];
	unsigned long	m_nRecordRate;
	unsigned long	m_nShutterSpeed;
	unsigned long	m_nTriggerMode;
	unsigned long	m_nManualFrames;
	unsigned long	m_nRandomFrames;
	unsigned long	m_nRandomManualFrames;
	unsigned long	m_nRandomTimes;
	unsigned long	m_nTwoStageType;
	unsigned long	m_nTwoStageLHFrame;
	unsigned long	m_nTwoStageCycle;
	unsigned long	m_nTwoStageHLFrame;
	unsigned short	m_nColorTemperature;
	unsigned short	m_nColorBalanceR;
	unsigned short	m_nColorBalanceG;
	unsigned short	m_nColorBalanceB;
	unsigned short	m_nColorBalanceBase;
	unsigned short	m_nColorBalanceMax;
	unsigned long	m_nOriginalTotalFrames;
	unsigned long	m_nTotalFrames;
	long			m_nStartFrame;
	long			m_nTriggerFrame;
	unsigned long	m_nNumOfEvent;
	long			m_nEvent[10];
	unsigned short	m_nWidth;
	unsigned short	m_nHeight;
	unsigned short	m_nSensorPosX;
	unsigned short	m_nSensorPosY;
	unsigned short	m_nSensorWidth;
	unsigned short	m_nSensorHeight;
	unsigned short	m_nColorType;
	unsigned short	m_nColorBits;
	unsigned short	m_nEffectiveBitDepth;
	unsigned short	m_nEffectiveBitSide;
	unsigned long	m_nIRIGMode;
	unsigned long	m_nShutterType2;
	short			m_nColorMatrixRR;
	short			m_nColorMatrixRG;
	short			m_nColorMatrixRB;
	short			m_nColorMatrixGR;
	short			m_nColorMatrixGG;
	short			m_nColorMatrixGB;
	short			m_nColorMatrixBR;
	short			m_nColorMatrixBG;
	short			m_nColorMatrixBB;
	unsigned short	m_nLUTBits;
	unsigned short	m_nColorEnhance;
	unsigned short	m_nEdgeEnhance;
	unsigned long	m_nLUTMode;
	unsigned short	m_nDSShutter;
	unsigned short	m_nPolarization;
	unsigned short	m_nPolarizerConfig;
	unsigned short	m_nDigitsOfFileNumber;
	unsigned short	m_nPixelGainBase;
	unsigned short	m_nPixelGainBits;
	unsigned short	m_nShadingBits;
	unsigned short	m_nBayerPattern;
	unsigned short	m_nExposeTimeNum;
	unsigned short	m_nRecOnCmdTimes;
	unsigned short	m_nPixelGainParam;
	unsigned short	m_nReserve;
	char			m_pDataName[64];
	unsigned long	m_IrigSample;
	unsigned long	m_AEExposureTimeRecordMode;
	unsigned short	m_AEModeSet;
	unsigned short	m_nDAQMode;
	unsigned long	m_nDAQRange[2];
	long			m_IrigOffset;
	unsigned long long	m_nSerialNumber;
	unsigned long	m_nDataNumber;			// 0:None 1<=:Data Number
	unsigned long	m_nIsOverSync;
	unsigned short	m_nExtOthersMode;
	unsigned short	m_nReserve2;
	unsigned long	m_nTemperatureType;		// 0:None 1:Type1 ...
	unsigned long	m_nAccelerationType;	// 0:None 1:Type1 ...
	unsigned long   m_nPixelGainDataSize;
} PDC_RECORD_INFO, *PPDC_RECORD_INFO;


/*
* Low Light backup
*/
typedef struct {
	unsigned long	m_nCamMode;
	unsigned long	m_nRecordRate;
	unsigned long	m_nWidth;
	unsigned long	m_nHeight;
	unsigned long	m_nShutterSpeedFps;
	unsigned long	m_nCurrentVariableChannel;
	unsigned long	m_nAutoExposure;
	unsigned long	m_nLowLightShutterSpeedFps;
} PDC_LOW_LIGHT_BACKUP_CHILD, *PPDC_LOW_LIGHT_BACKUP_CHILD;


typedef struct {
	unsigned long	m_nExternalIn[PDC_EXTIO_MAX_PORT];
	unsigned long	m_nTriggerMode;			
	unsigned long	m_nTriggerAfterFrames;	
	unsigned long	m_nTriggerRandomFrames;	
	unsigned long	m_nTriggerRandomCount;	
	PDC_LOW_LIGHT_BACKUP_CHILD m_ChildInfo[PDC_MAX_CHILD_DEVICE];
} PDC_LOW_LIGHT_BACKUP, *PPDC_LOW_LIGHT_BACKUP;

typedef struct {
    const char*     pFileFormat;
    const char*     pColorType;
    unsigned long   colorDepth;
} PDC_ARCHIVE_PARAM, *PPDC_ARCHIVE_PARAM;

typedef struct {
	PDC_ARCHIVE_OPTION_TYPE type;
	void*					pOption;
	unsigned long			count;
} PDC_ARCHIVE_OPTION, *PPDC_ARCHIVE_OPTION;

typedef struct {
    const char*	pKey;
    const char*	pValue;
} PDC_ARCHIVE_OPTION_META, *PPDC_ARCHIVE_OPTION_META;

typedef struct {
	PDC_ARCHIVE_DATA_TYPE	type;
	unsigned long long		size;
	char*					pData;
} PDC_ARCHIVE_OPTION_BIN, *PPDC_ARCHIVE_OPTION_BIN;

typedef struct {
	unsigned long long	size;
	char*				pData;
} PDC_ARCHIVE_OPTION_XML, *PPDC_ARCHIVE_OPTION_XML;

typedef struct {
	unsigned long long	count;
	long*				pFrames;
} PDC_ARCHIVE_OPTION_MAPFRAME, *PPDC_ARCHIVE_OPTION_MAPFRAME;

typedef struct {
	PDC_ARCHIVE_DATA_TYPE	type;
	unsigned long long		offset;
	unsigned long long		size;
} PDC_ARCHIVE_DATA_HEAD, *PPDC_ARCHIVE_DATA_HEAD;

typedef struct {
	unsigned long nParamType;
	unsigned long nParamKey;
	unsigned long nParamValue;
} PDC_OPEN_INFO, *PPDC_OPEN_INFO;

#pragma pack()
#endif	/*	_PDC_STR_H_	*/