/* Generated from test.scm by the CHICKEN compiler
   http://www.call-cc.org
   2018-02-13 22:03
   Version 4.9.0.1 (stability/4.9.0) (rev 8b3189b)
   windows-mingw32-x86 [ manyargs dload ptables ]
   bootstrapped 2014-06-07
   command line: test.scm -output-file run_time.c -optimize-level 3
   used units: library eval chicken_2dsyntax
*/

#include "chicken.h"

static C_PTABLE_ENTRY *create_ptable(void);
C_noret_decl(C_library_toplevel)
C_externimport void C_ccall C_library_toplevel(C_word c,C_word d,C_word k) C_noret;
C_noret_decl(C_eval_toplevel)
C_externimport void C_ccall C_eval_toplevel(C_word c,C_word d,C_word k) C_noret;
C_noret_decl(C_chicken_2dsyntax_toplevel)
C_externimport void C_ccall C_chicken_2dsyntax_toplevel(C_word c,C_word d,C_word k) C_noret;

static C_TLS C_word lf[4];
static double C_possibly_force_alignment;
static C_char C_TLS li0[] C_aligned={C_lihdr(0,0,10),40,116,111,112,108,101,118,101,108,41,0,0,0,0,0,0};


C_noret_decl(f_191)
static void C_ccall f_191(C_word c,C_word t0,C_word t1) C_noret;
C_noret_decl(C_toplevel)
C_externexport void C_ccall C_toplevel(C_word c,C_word t0,C_word t1) C_noret;
C_noret_decl(f_184)
static void C_ccall f_184(C_word c,C_word t0,C_word t1) C_noret;
C_noret_decl(f_187)
static void C_ccall f_187(C_word c,C_word t0,C_word t1) C_noret;
C_noret_decl(f_194)
static void C_ccall f_194(C_word c,C_word t0,C_word t1) C_noret;
C_noret_decl(f_197)
static void C_ccall f_197(C_word c,C_word t0,C_word t1) C_noret;
C_noret_decl(f_181)
static void C_ccall f_181(C_word c,C_word t0,C_word t1) C_noret;

C_noret_decl(tr2)
static void C_fcall tr2(C_proc2 k) C_regparm C_noret;
C_regparm static void C_fcall tr2(C_proc2 k){
C_word t1=C_pick(0);
C_word t0=C_pick(1);
C_adjust_stack(-2);
(k)(2,t0,t1);}

/* k189 in k185 in k182 in k179 */
static void C_ccall f_191(C_word c,C_word t0,C_word t1){
C_word tmp;
C_word t2;
C_word t3;
C_word t4;
C_word t5;
C_word ab[6],*a=ab;
C_check_for_interrupt;
if(!C_stack_probe(&a)){
C_save_and_reclaim((void*)tr2,(void*)f_191,2,t0,t1);}
t2=C_mutate2((C_word*)lf[0]+1 /* (set! hi ...) */,t1);
t3=(*a=C_CLOSURE_TYPE|2,a[1]=(C_word)f_194,a[2]=((C_word*)t0)[2],tmp=(C_word)a,a+=3,tmp);
t4=(*a=C_CLOSURE_TYPE|2,a[1]=(C_word)f_197,a[2]=t3,tmp=(C_word)a,a+=3,tmp);
C_trace("##sys#implicit-exit-handler");
((C_proc2)C_fast_retrieve_symbol_proc(lf[1]))(2,*((C_word*)lf[1]+1),t4);}

/* toplevel */
static C_TLS int toplevel_initialized=0;
C_main_entry_point
C_noret_decl(toplevel_trampoline)
static void C_fcall toplevel_trampoline(void *dummy) C_regparm C_noret;
C_regparm static void C_fcall toplevel_trampoline(void *dummy){
C_toplevel(2,C_SCHEME_UNDEFINED,C_restore);}

void C_ccall C_toplevel(C_word c,C_word t0,C_word t1){
C_word tmp;
C_word t2;
C_word t3;
C_word *a;
if(toplevel_initialized) C_kontinue(t1,C_SCHEME_UNDEFINED);
else C_toplevel_entry(C_text("toplevel"));
C_check_nursery_minimum(3);
if(!C_demand(3)){
C_save(t1);
C_reclaim((void*)toplevel_trampoline,NULL);}
toplevel_initialized=1;
if(!C_demand_2(30)){
C_save(t1);
C_rereclaim2(30*sizeof(C_word), 1);
t1=C_restore;}
a=C_alloc(3);
C_initialize_lf(lf,4);
lf[0]=C_h_intern(&lf[0],2,"hi");
lf[1]=C_h_intern(&lf[1],25,"\003sysimplicit-exit-handler");
lf[2]=C_h_intern(&lf[2],5,"print");
lf[3]=C_decode_literal(C_heaptop,"\376B\000\000\002hi");
C_register_lf2(lf,4,create_ptable());
t2=(*a=C_CLOSURE_TYPE|2,a[1]=(C_word)f_181,a[2]=t1,tmp=(C_word)a,a+=3,tmp);
C_library_toplevel(2,C_SCHEME_UNDEFINED,t2);}

/* k182 in k179 */
static void C_ccall f_184(C_word c,C_word t0,C_word t1){
C_word tmp;
C_word t2;
C_word t3;
C_word ab[3],*a=ab;
C_check_for_interrupt;
if(!C_stack_probe(&a)){
C_save_and_reclaim((void*)tr2,(void*)f_184,2,t0,t1);}
t2=(*a=C_CLOSURE_TYPE|2,a[1]=(C_word)f_187,a[2]=((C_word*)t0)[2],tmp=(C_word)a,a+=3,tmp);
C_chicken_2dsyntax_toplevel(2,C_SCHEME_UNDEFINED,t2);}

/* k185 in k182 in k179 */
static void C_ccall f_187(C_word c,C_word t0,C_word t1){
C_word tmp;
C_word t2;
C_word t3;
C_word ab[3],*a=ab;
C_check_for_interrupt;
if(!C_stack_probe(&a)){
C_save_and_reclaim((void*)tr2,(void*)f_187,2,t0,t1);}
t2=(*a=C_CLOSURE_TYPE|2,a[1]=(C_word)f_191,a[2]=((C_word*)t0)[2],tmp=(C_word)a,a+=3,tmp);
C_trace("test.scm:20: print");
t3=*((C_word*)lf[2]+1);
((C_proc3)(void*)(*((C_word*)t3+1)))(3,t3,t2,lf[3]);}

/* k192 in k189 in k185 in k182 in k179 */
static void C_ccall f_194(C_word c,C_word t0,C_word t1){
C_word tmp;
C_word t2;
C_word *a;
t2=((C_word*)t0)[2];
((C_proc2)(void*)(*((C_word*)t2+1)))(2,t2,C_SCHEME_UNDEFINED);}

/* k195 in k189 in k185 in k182 in k179 */
static void C_ccall f_197(C_word c,C_word t0,C_word t1){
C_word tmp;
C_word t2;
C_word *a;
t2=t1;
((C_proc2)C_fast_retrieve_proc(t2))(2,t2,((C_word*)t0)[2]);}

/* k179 */
static void C_ccall f_181(C_word c,C_word t0,C_word t1){
C_word tmp;
C_word t2;
C_word t3;
C_word ab[3],*a=ab;
C_check_for_interrupt;
if(!C_stack_probe(&a)){
C_save_and_reclaim((void*)tr2,(void*)f_181,2,t0,t1);}
t2=(*a=C_CLOSURE_TYPE|2,a[1]=(C_word)f_184,a[2]=((C_word*)t0)[2],tmp=(C_word)a,a+=3,tmp);
C_eval_toplevel(2,C_SCHEME_UNDEFINED,t2);}

#ifdef C_ENABLE_PTABLES
static C_PTABLE_ENTRY ptable[8] = {
{"f_191:test_2escm",(void*)f_191},
{"toplevel:test_2escm",(void*)C_toplevel},
{"f_184:test_2escm",(void*)f_184},
{"f_187:test_2escm",(void*)f_187},
{"f_194:test_2escm",(void*)f_194},
{"f_197:test_2escm",(void*)f_197},
{"f_181:test_2escm",(void*)f_181},
{NULL,NULL}};
#endif

static C_PTABLE_ENTRY *create_ptable(void){
#ifdef C_ENABLE_PTABLES
return ptable;
#else
return NULL;
#endif
}

/*
o|removed binding forms: 5 
*/
/* end of file */
