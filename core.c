/*
# *****************************************************************************
#
# Filename    :    core.c
# Description :    core functions
# Version     :    1.0
# Authors     :    Diego Paris
# e-mail      :    diego.paris@inaf.it
# Last modify :    05/01/2023
# Copyright   :    (C) 2023 JWST GLASS-ERS Team
# License     :	   GNU General Public License
# 
#******************************************************************************
#
# This is a free software coming WITHOUT ANY WARRANTY and you can redistribute 
# it and/or modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation. You should have received a copy 
# of the GNU General Public License along with it. 
# If not, see <http://www.gnu.org/licenses/>.
#
# *****************************************************************************

*/
#include <string.h>
#include <stdio.h>
#include <fitsio.h>
#include <errno.h>
#include "core.h"

typedef unsigned int uint;

int dilate(char *flag, char *msk, short dil, short factor, unsigned short mod, uint v){
  fitsfile *inflagptr;
  fitsfile *outmskptr;
  char *inrow;
  int *outrow;
  int status=0;
  int naxis;
  long naxes[2];
  long firstpix[2] = {1,1};
  short dilation = (mod==9) ? (dil*factor) : dil;
  short iter = (dilation/2)>0 ? (dilation/2) : 1;
  int errval;
  int **data;
  int **dilated;
  int j,ii,jj;
  int w=1;
  int **swap;
  int sum;
  int K = (mod==9) ? 9 : 3;
  int kernel3[3][3]={{0, 1, 0}, 
		     {1, 1, 1}, 
		     {0, 1, 0}};
  int kernel9[9][9]={{0, 0, 0, 0, 1, 0, 0, 0, 0}, 
		     {0, 0, 0, 1, 1, 1, 0, 0, 0}, 
		     {0, 0, 1, 1, 1, 1, 1, 0, 0}, 
		     {0, 1, 1, 1, 1, 1, 1, 1, 0}, 
		     {1, 1, 1, 1, 1, 1, 1, 1, 1}, 
		     {0, 1, 1, 1, 1, 1, 1, 1, 0}, 
		     {0, 0, 1, 1, 1, 1, 1, 0, 0},  
		     {0, 0, 0, 1, 1, 1, 0, 0, 0}, 
		     {0, 0, 0, 0, 1, 0, 0, 0, 0}};
	
  if(fits_open_file(&inflagptr, flag, READONLY, &status)) {
    fits_report_error(stderr, status);
    return(RETURN_FAILURE);
  }
  if (fits_create_file(&outmskptr, msk, &status)) {
    fits_report_error(stderr, status);
    return(RETURN_FAILURE);
  }  
  if (fits_get_img_dim(inflagptr, &naxis, &status)) {
    fits_report_error(stderr, status);
    return(RETURN_FAILURE);
  }
  if (fits_get_img_size(inflagptr, 2, naxes, &status)) {
    fits_report_error(stderr, status);
    return(RETURN_FAILURE);
  }
  if (fits_copy_header(inflagptr, outmskptr, &status)) {
    fits_report_error(stderr, status);
    return(RETURN_FAILURE);  
  } 
  QMALLOC(inrow, char, naxes[0]*sizeof(int), errval);
  QMALLOC2D(data,int,naxes[0],naxes[1],errval);
  QMALLOC2D(dilated,int,naxes[0],naxes[1],errval);
  int i;
  for (firstpix[1] = 1;firstpix[1]<=naxes[1];firstpix[1]++){
    if (fits_read_pix(inflagptr, TINT, firstpix, naxes[0], NULL, (void *) inrow, NULL, &status)){
      fits_report_error(stderr, status);
      return(RETURN_FAILURE);
    }
    int *tin;
    for (i=0; i < naxes[0]; i++){ 
      tin = (int *)((char *) inrow + i * sizeof(int));
      data[i][(firstpix[1]-1)] = (int)*tin;
    }                           
  }
  if (mod==9){
    if (v==1){
      printf("Convolving edges with kernel:\n");  
      for(int i = 0; i < 9; i++) {
	 for(int j = 0; j < 9; j++) {
	     printf("%d ", kernel9[i][j]);
	 }
	 printf("\n");
       }      	    
    }
    while(TRUE){
      int pct = ((float) w / iter) * 100;
      for (j = K / 2; j < naxes[1] - K / 2; ++j) { 
	for (i = K / 2; i < naxes[0] - K / 2; ++i){
	  sum = 0; 
	  for (jj = - K / 2; jj <= K / 2; ++jj){ 
	    for (ii = - K / 2; ii <= K / 2; ++ii) {
	      int intdata = data[i + ii][j +jj]; 
	      int coeff = kernel9[ii + K / 2][jj + K / 2];
	      sum += intdata * coeff;
	    }
	  }
	  dilated[i][j] = sum ? 1 : 0; 
	}
      }
      if (w==iter) break;
      SWAP(dilated,data,swap); 
      w++;
    }
  } else {
    if (v==1){
      printf("Convolving edges with kernel:\n"); 
      for(int i = 0; i < 3; i++) {
	for(int j = 0; j < 3; j++) {
	  printf("%d ", kernel3[i][j]);
	}
	printf("\n");
      }    	    
    }
    while(TRUE){
      for (j = K / 2; j < naxes[1] - K / 2; ++j) { 
	for (i = K / 2; i < naxes[0] - K / 2; ++i){
	  sum = 0; 
	  for (jj = - K / 2; jj <= K / 2; ++jj){ 
	    for (ii = - K / 2; ii <= K / 2; ++ii) {
	      int intdata = data[i + ii][j +jj]; 
	      int coeff = kernel3[ii + K / 2][jj + K / 2];
	      sum += intdata * coeff;
	    }
	  }
	  dilated[i][j] = sum ? 1 : 0; 
	}
      }
      if (w==iter) break;
      SWAP(dilated,data,swap); 
      w++;
    }
  }
  QMALLOC(outrow, int, naxes[0], errval); 
  for (firstpix[1] = 1;firstpix[1]<=naxes[1];firstpix[1]++){ 
    int *tout=outrow;
    for (i=0; i < naxes[0]; i++){
      *tout = dilated[i][(firstpix[1]-1)];
      tout++;
    }       
    if (fits_write_pix(outmskptr, TINT, firstpix, 
		       naxes[0], (void *)outrow, &status)) {
      fits_report_error(stderr, status);
      return(RETURN_FAILURE);
    }
  }
  for (i=0;i<naxes[0];i++){
    QFREE(data[i]);
    QFREE(dilated[i]); 
  }
  QFREE(data);
  QFREE(dilated);
  QFREE(outrow);
  QFREE(inrow);  
  if (fits_close_file(inflagptr, &status)) {
    fits_report_error(stderr, status);
    return(RETURN_FAILURE);
  }
  if(fits_close_file(outmskptr, &status)) {
    fits_report_error(stderr, status);
    return(RETURN_FAILURE);
  }  
}
