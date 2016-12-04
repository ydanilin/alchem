/* The wrapper (extern "C" { )*/
SWIGINTERN PyObject *_wrap_agopen(PyObject *SWIGUNUSEDPARM(self), PyObject *args) {
  PyObject *resultobj = 0;
  char *arg1 = (char *) 0 ;
  Agdesc_t arg2 ;
  Agdisc_t *arg3 = (Agdisc_t *) 0 ;
  int res1 ;
  char *buf1 = 0 ;
  int alloc1 = 0 ;
  void *argp2 ;
  int res2 = 0 ;
  void *argp3 = 0 ;
  int res3 = 0 ;
  PyObject * obj0 = 0 ;
  PyObject * obj1 = 0 ;
  PyObject * obj2 = 0 ;
  Agraph_t *result = 0 ;
  
  if (!PyArg_ParseTuple(args,(char *)"OOO:agopen",&obj0,&obj1,&obj2)) SWIG_fail;
  res1 = SWIG_AsCharPtrAndSize(obj0, &buf1, NULL, &alloc1);
  if (!SWIG_IsOK(res1)) {
    SWIG_exception_fail(SWIG_ArgError(res1), "in method '" "agopen" "', argument " "1"" of type '" "char *""'");
  }
  arg1 = (char *)(buf1);
  {
    res2 = SWIG_ConvertPtr(obj1, &argp2, SWIGTYPE_p_Agdesc_t,  0 );
    if (!SWIG_IsOK(res2)) {
      SWIG_exception_fail(SWIG_ArgError(res2), "in method '" "agopen" "', argument " "2"" of type '" "Agdesc_t""'"); 
    }  
    if (!argp2) {
      SWIG_exception_fail(SWIG_ValueError, "invalid null reference " "in method '" "agopen" "', argument " "2"" of type '" "Agdesc_t""'");
    } else {
      arg2 = *((Agdesc_t *)(argp2));
    }
  }
  res3 = SWIG_ConvertPtr(obj2, &argp3,SWIGTYPE_p_Agdisc_t, 0 |  0 );
  if (!SWIG_IsOK(res3)) {
    SWIG_exception_fail(SWIG_ArgError(res3), "in method '" "agopen" "', argument " "3"" of type '" "Agdisc_t *""'"); 
  }
  arg3 = (Agdisc_t *)(argp3);
  result = (Agraph_t *)agopen(arg1,arg2,arg3);
  resultobj = SWIG_NewPointerObj(SWIG_as_voidptr(result), SWIGTYPE_p_Agraph_t, 0 |  0 );
  if (alloc1 == SWIG_NEWOBJ) free((char*)buf1);
  return resultobj;
fail:
  if (alloc1 == SWIG_NEWOBJ) free((char*)buf1);
  return NULL;
}

/* SWIG_AsCharPtrAndSize */
SWIGINTERN int
SWIG_AsCharPtrAndSize(PyObject *obj, char** cptr, size_t* psize, int *alloc)
{
#if PY_VERSION_HEX>=0x03000000
  if (PyBytes_Check(obj))
#else  
  if (PyString_Check(obj))
#endif
  {
    char *cstr; Py_ssize_t len;
#if PY_VERSION_HEX>=0x03000000
    PyBytes_AsStringAndSize(obj, &cstr, &len);
    if(alloc) *alloc = SWIG_NEWOBJ;
#else
    PyString_AsStringAndSize(obj, &cstr, &len);
#endif
    if (cptr) {
      if (alloc) {
	/* 
	   In python the user should not be able to modify the inner
	   string representation. To warranty that, if you define
	   SWIG_PYTHON_SAFE_CSTRINGS, a new/copy of the python string
	   buffer is always returned.

	   The default behavior is just to return the pointer value,
	   so, be careful.
	*/ 
#if defined(SWIG_PYTHON_SAFE_CSTRINGS)
	if (*alloc != SWIG_OLDOBJ) 
#else
	if (*alloc == SWIG_NEWOBJ) 
#endif
	  {
	    *cptr = (char *)memcpy((char *)malloc((len + 1)*sizeof(char)), cstr, sizeof(char)*(len + 1));
	    *alloc = SWIG_NEWOBJ;
	  }
	else {
	  *cptr = cstr;
	  *alloc = SWIG_OLDOBJ;
	}
      } else {
	*cptr = SWIG_Python_str_AsChar(obj);
      }
    }
    if (psize) *psize = len + 1;
    return SWIG_OK;
  } else {
    swig_type_info* pchar_descriptor = SWIG_pchar_descriptor();
    if (pchar_descriptor) {
      void* vptr = 0;
      if (SWIG_ConvertPtr(obj, &vptr, pchar_descriptor, 0) == SWIG_OK) {
	if (cptr) *cptr = (char *) vptr;
	if (psize) *psize = vptr ? (strlen((char *)vptr) + 1) : 0;
	if (alloc) *alloc = SWIG_OLDOBJ;
	return SWIG_OK;
      }
    }
  }
  return SWIG_TypeError;
}


#define SWIG_IsOK(r)               (r >= 0)
#define SWIG_ArgError(r)           ((r != SWIG_ERROR) ? r : SWIG_TypeError)
#define SWIG_ConvertPtr(obj, pptr, type, flags)         SWIG_Python_ConvertPtr(obj, pptr, type, flags)
#define SWIGTYPE_p_Agdesc_t swig_types[0]

#include "C:/Program Files (x86)/Graphviz2.38/include/graphviz/cgraph.h"

/* Convert a pointer value */

SWIGRUNTIME int
SWIG_Python_ConvertPtrAndOwn(PyObject *obj, void **ptr, swig_type_info *ty, int flags, int *own) {
  int res;
  SwigPyObject *sobj;
  int implicit_conv = (flags & SWIG_POINTER_IMPLICIT_CONV) != 0;

  if (!obj)
    return SWIG_ERROR;
  if (obj == Py_None && !implicit_conv) {
    if (ptr)
      *ptr = 0;
    return SWIG_OK;
  }

  res = SWIG_ERROR;

  sobj = SWIG_Python_GetSwigThis(obj);
  if (own)
    *own = 0;
  while (sobj) {
    void *vptr = sobj->ptr;
    if (ty) {
      swig_type_info *to = sobj->ty;
      if (to == ty) {
        /* no type cast needed */
        if (ptr) *ptr = vptr;
        break;
      } else {
        swig_cast_info *tc = SWIG_TypeCheck(to->name,ty);
        if (!tc) {
          sobj = (SwigPyObject *)sobj->next;
        } else {
          if (ptr) {
            int newmemory = 0;
            *ptr = SWIG_TypeCast(tc,vptr,&newmemory);
            if (newmemory == SWIG_CAST_NEW_MEMORY) {
              assert(own); /* badly formed typemap which will lead to a memory leak - it must set and use own to delete *ptr */
              if (own)
                *own = *own | SWIG_CAST_NEW_MEMORY;
            }
          }
          break;
        }
      }
    } else {
      if (ptr) *ptr = vptr;
      break;
    }
  }
  if (sobj) {
    if (own)
      *own = *own | sobj->own;
    if (flags & SWIG_POINTER_DISOWN) {
      sobj->own = 0;
    }
    res = SWIG_OK;
  } else {
    if (implicit_conv) {
      SwigPyClientData *data = ty ? (SwigPyClientData *) ty->clientdata : 0;
      if (data && !data->implicitconv) {
        PyObject *klass = data->klass;
        if (klass) {
          PyObject *impconv;
          data->implicitconv = 1; /* avoid recursion and call 'explicit' constructors*/
          impconv = SWIG_Python_CallFunctor(klass, obj);
          data->implicitconv = 0;
          if (PyErr_Occurred()) {
            PyErr_Clear();
            impconv = 0;
          }
          if (impconv) {
            SwigPyObject *iobj = SWIG_Python_GetSwigThis(impconv);
            if (iobj) {
              void *vptr;
              res = SWIG_Python_ConvertPtrAndOwn((PyObject*)iobj, &vptr, ty, 0, 0);
              if (SWIG_IsOK(res)) {
                if (ptr) {
                  *ptr = vptr;
                  /* transfer the ownership to 'ptr' */
                  iobj->own = 0;
                  res = SWIG_AddCast(res);
                  res = SWIG_AddNewMask(res);
                } else {
                  res = SWIG_AddCast(res);		    
                }
              }
            }
            Py_DECREF(impconv);
          }
        }
      }
    }
    if (!SWIG_IsOK(res) && obj == Py_None) {
      if (ptr)
        *ptr = 0;
      if (PyErr_Occurred())
        PyErr_Clear();
      res = SWIG_OK;
    }
  }
  return res;
}
