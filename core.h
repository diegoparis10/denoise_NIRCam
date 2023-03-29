/*
# *****************************************************************************
#
# Filename    :    core.h
# Description :    header file of core.c
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

/*                           Internal constants                              */
#define TRUE 1
#define FALSE 0
/*                              Return messages                              */
#define	RETURN_SUCCESS		0
#define	RETURN_FAILURE		-1
/*                               Macros                               */
#define SWAP(a,b,tmp) { tmp = a; a = b; b = tmp;}
/*                           Allocation macros                               */
#define	QMALLOC(ptr, type, n, errv) {                                         \
    if(!(ptr=(type *)malloc((size_t)(n)*sizeof(type)))) {		      \
      errv = errno;							      \
      fprintf(stderr, "%s:%d: %s\n", __FUNCTION__, __LINE__, strerror(errv)); \
      exit(EXIT_FAILURE);                                                     \
    }                                                                         \
  }
#define	QCALLOC(ptr, type, n, errv) {                                         \
    if(!(ptr=(type *)calloc((size_t)(n),sizeof(type)))) {		      \
      errv = errno;							      \
      fprintf(stderr, "%s:%d: %s\n", __FUNCTION__, __LINE__, strerror(errv)); \
      exit(EXIT_FAILURE);                                                     \
    }                                                                         \
  }
#define	QREALLOC(ptr, type, n, errv) {                                        \
    if(!(ptr=(type *)realloc(ptr,(size_t)(n)*sizeof(type)))) {		      \
      errv = errno;							      \
      fprintf(stderr, "%s:%d: %s\n", __FUNCTION__, __LINE__, strerror(errv)); \
      exit(EXIT_FAILURE);                                                     \
    }                                                                         \
  }
#define	QFREE(ptr) {        \
    free(ptr);              \
    ptr = NULL;             \
  }
#define QMALLOC2D(ptr, typ, nlins, ncols, errv)                               \
                {int i; QMALLOC(ptr, typ *, nlins, errv);                     \
                 for (i=0; i < nlins; i++)                                    \
                       QMALLOC(ptr[i], typ, ncols, errv);;}                   \
                       
                       
