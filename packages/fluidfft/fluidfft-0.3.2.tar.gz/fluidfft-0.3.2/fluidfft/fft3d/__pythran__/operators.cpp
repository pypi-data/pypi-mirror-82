#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/include/builtins/None.hpp>
#include <pythonic/include/builtins/abs.hpp>
#include <pythonic/include/builtins/getattr.hpp>
#include <pythonic/include/builtins/int_.hpp>
#include <pythonic/include/builtins/len.hpp>
#include <pythonic/include/builtins/pythran/make_shape.hpp>
#include <pythonic/include/builtins/range.hpp>
#include <pythonic/include/builtins/round.hpp>
#include <pythonic/include/builtins/tuple.hpp>
#include <pythonic/include/numpy/sqrt.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/operator_/add.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/operator_/ge.hpp>
#include <pythonic/include/operator_/iadd.hpp>
#include <pythonic/include/operator_/isub.hpp>
#include <pythonic/include/operator_/mul.hpp>
#include <pythonic/include/operator_/sub.hpp>
#include <pythonic/include/types/complex.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/builtins/None.hpp>
#include <pythonic/builtins/abs.hpp>
#include <pythonic/builtins/getattr.hpp>
#include <pythonic/builtins/int_.hpp>
#include <pythonic/builtins/len.hpp>
#include <pythonic/builtins/pythran/make_shape.hpp>
#include <pythonic/builtins/range.hpp>
#include <pythonic/builtins/round.hpp>
#include <pythonic/builtins/tuple.hpp>
#include <pythonic/numpy/sqrt.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/operator_/add.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/operator_/ge.hpp>
#include <pythonic/operator_/iadd.hpp>
#include <pythonic/operator_/isub.hpp>
#include <pythonic/operator_/mul.hpp>
#include <pythonic/operator_/sub.hpp>
#include <pythonic/types/complex.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_operators
{
  struct __transonic__
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef pythonic::types::str __type0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type0>()))>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type2;
      typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type5;
      typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type5>())) __type6;
      typedef decltype(pythonic::operator_::sub(std::declval<__type3>(), std::declval<__type6>())) __type7;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type7>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& vx_fft, argument_type3&& vy_fft) const
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 , typename argument_type7 , typename argument_type8 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type3>())) __type4;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
      typedef typename pythonic::lazy<__type5>::type __type6;
      typedef decltype(std::declval<__type2>()(std::declval<__type6>())) __type7;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type4>::type>::type __type9;
      typedef typename pythonic::lazy<__type9>::type __type10;
      typedef decltype(std::declval<__type2>()(std::declval<__type10>())) __type11;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type4>::type>::type __type13;
      typedef typename pythonic::lazy<__type13>::type __type14;
      typedef decltype(std::declval<__type2>()(std::declval<__type14>())) __type15;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type15>::type::iterator>::value_type>::type __type16;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type8>(), std::declval<__type12>(), std::declval<__type16>())) __type17;
      typedef decltype(std::declval<__type1>()[std::declval<__type17>()]) __type18;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type19;
      typedef decltype(std::declval<__type19>()[std::declval<__type17>()]) __type20;
      typedef decltype(pythonic::operator_::mul(std::declval<__type18>(), std::declval<__type20>())) __type21;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type22;
      typedef decltype(std::declval<__type22>()[std::declval<__type17>()]) __type23;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type24;
      typedef decltype(std::declval<__type24>()[std::declval<__type17>()]) __type25;
      typedef decltype(pythonic::operator_::mul(std::declval<__type23>(), std::declval<__type25>())) __type26;
      typedef decltype(pythonic::operator_::sub(std::declval<__type21>(), std::declval<__type26>())) __type27;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type27>())) __type28;
      typedef __type28 __ptype0;
      typedef __type17 __ptype1;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 , typename argument_type7 , typename argument_type8 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6, argument_type7, argument_type8>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& vx_fft, argument_type4&& vy_fft, argument_type5&& vz_fft, argument_type6&& rotxfft, argument_type7&& rotyfft, argument_type8&& rotzfft) const
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type2;
      typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type5;
      typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type5>())) __type6;
      typedef decltype(pythonic::operator_::sub(std::declval<__type3>(), std::declval<__type6>())) __type7;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type7>())) __type8;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type9;
      typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type11;
      typedef decltype(pythonic::operator_::mul(std::declval<__type11>(), std::declval<__type2>())) __type12;
      typedef decltype(pythonic::operator_::sub(std::declval<__type10>(), std::declval<__type12>())) __type13;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type13>())) __type14;
      typedef decltype(pythonic::operator_::mul(std::declval<__type11>(), std::declval<__type5>())) __type15;
      typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type9>())) __type16;
      typedef decltype(pythonic::operator_::sub(std::declval<__type15>(), std::declval<__type16>())) __type17;
      typedef decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type17>())) __type18;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type8>(), std::declval<__type14>(), std::declval<__type18>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& vx_fft, argument_type4&& vy_fft, argument_type5&& vz_fft) const
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__divfft_from_vecfft
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type2;
      typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type5;
      typedef decltype(pythonic::operator_::mul(std::declval<__type4>(), std::declval<__type5>())) __type6;
      typedef decltype(pythonic::operator_::add(std::declval<__type3>(), std::declval<__type6>())) __type7;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type8;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type9;
      typedef decltype(pythonic::operator_::mul(std::declval<__type8>(), std::declval<__type9>())) __type10;
      typedef decltype(pythonic::operator_::add(std::declval<__type7>(), std::declval<__type10>())) __type11;
      typedef typename pythonic::returnable<decltype(pythonic::operator_::mul(std::declval<__type0>(), std::declval<__type11>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& vx_fft, argument_type4&& vy_fft, argument_type5&& vz_fft) const
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__project_perpk3d
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type1;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type2;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type3;
      typedef typename pythonic::lazy<__type3>::type __type4;
      typedef decltype(std::declval<__type0>()(std::declval<__type4>())) __type5;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type __type6;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type7;
      typedef typename pythonic::lazy<__type7>::type __type8;
      typedef decltype(std::declval<__type0>()(std::declval<__type8>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type2>::type>::type __type11;
      typedef typename pythonic::lazy<__type11>::type __type12;
      typedef decltype(std::declval<__type0>()(std::declval<__type12>())) __type13;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type13>::type::iterator>::value_type>::type __type14;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type6>(), std::declval<__type10>(), std::declval<__type14>())) __type15;
      typedef __type15 __ptype12;
      typedef __type15 __ptype13;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& self_inv_K_square_nozero, argument_type4&& vx_fft, argument_type5&& vy_fft, argument_type6&& vz_fft) const
    ;
  }  ;
  struct __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop
  {
    typedef void callable;
    typedef void pure;
    struct type
    {
      typedef typename pythonic::returnable<pythonic::types::str>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  struct __for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type6>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type1;
      typedef __type0 __ptype24;
      typedef __type1 __ptype25;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6>::result_type operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& self_inv_K_square_nozero, argument_type4&& vx_fft, argument_type5&& vy_fft, argument_type6&& vz_fft) const
    ;
  }  ;
  struct loop_spectra_kzkh
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type0>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type2;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type5;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type6;
      typedef container<typename std::remove_reference<__type3>::type> __type7;
      typedef typename __combined<__type2,__type7>::type __type8;
      typedef typename pythonic::assignable<decltype(std::declval<__type6>()(std::declval<__type8>()))>::type __type9;
      typedef container<typename std::remove_reference<__type1>::type> __type10;
      typedef typename __combined<__type0,__type10>::type __type11;
      typedef typename pythonic::assignable<decltype(std::declval<__type6>()(std::declval<__type11>()))>::type __type12;
      typedef decltype(std::declval<__type5>()(std::declval<__type9>(), std::declval<__type12>())) __type13;
      typedef typename pythonic::assignable<decltype(std::declval<__type4>()(std::declval<__type13>()))>::type __type14;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type15;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::round{})>::type>::type __type16;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type17;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type18;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type19;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type20;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type20>())) __type21;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type21>::type>::type __type22;
      typedef typename pythonic::lazy<__type22>::type __type23;
      typedef decltype(std::declval<__type19>()(std::declval<__type23>())) __type24;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type24>::type::iterator>::value_type>::type __type25;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type21>::type>::type __type26;
      typedef typename pythonic::lazy<__type26>::type __type27;
      typedef decltype(std::declval<__type19>()(std::declval<__type27>())) __type28;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type28>::type::iterator>::value_type>::type __type29;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type21>::type>::type __type30;
      typedef typename pythonic::lazy<__type30>::type __type31;
      typedef decltype(std::declval<__type19>()(std::declval<__type31>())) __type32;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type32>::type::iterator>::value_type>::type __type33;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type25>(), std::declval<__type29>(), std::declval<__type33>())) __type34;
      typedef decltype(std::declval<__type18>()[std::declval<__type34>()]) __type35;
      typedef decltype(std::declval<__type17>()(std::declval<__type35>())) __type36;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type>::type __type37;
      typedef decltype(pythonic::operator_::div(std::declval<__type36>(), std::declval<__type37>())) __type38;
      typedef decltype(std::declval<__type16>()(std::declval<__type38>())) __type39;
      typedef decltype(std::declval<__type15>()(std::declval<__type39>())) __type40;
      typedef typename pythonic::lazy<__type40>::type __type41;
      typedef long __type42;
      typedef decltype(pythonic::operator_::sub(std::declval<__type9>(), std::declval<__type42>())) __type43;
      typedef typename pythonic::lazy<__type43>::type __type44;
      typedef typename __combined<__type41,__type44>::type __type45;
      typedef decltype(pythonic::operator_::sub(std::declval<__type12>(), std::declval<__type42>())) __type46;
      typedef typename pythonic::lazy<__type46>::type __type47;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type45>(), std::declval<__type47>())) __type48;
      typedef indexable<__type48> __type49;
      typedef typename __combined<__type14,__type49>::type __type50;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type51;
      typedef typename pythonic::assignable<decltype(std::declval<__type51>()[std::declval<__type34>()])>::type __type52;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type0>::type>::type>::type __type53;
      typedef decltype(pythonic::operator_::div(std::declval<__type52>(), std::declval<__type53>())) __type54;
      typedef typename pythonic::assignable<decltype(std::declval<__type15>()(std::declval<__type54>()))>::type __type55;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type45>(), std::declval<__type55>())) __type56;
      typedef indexable<__type56> __type57;
      typedef typename __combined<__type50,__type57>::type __type58;
      typedef decltype(pythonic::operator_::add(std::declval<__type55>(), std::declval<__type42>())) __type59;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type45>(), std::declval<__type59>())) __type60;
      typedef indexable<__type60> __type61;
      typedef typename __combined<__type58,__type61>::type __type62;
      typedef typename pythonic::assignable<decltype(std::declval<__type20>()[std::declval<__type34>()])>::type __type63;
      typedef container<typename std::remove_reference<__type63>::type> __type64;
      typedef typename __combined<__type62,__type64>::type __type65;
      typedef decltype(std::declval<__type11>()[std::declval<__type55>()]) __type66;
      typedef decltype(pythonic::operator_::sub(std::declval<__type52>(), std::declval<__type66>())) __type67;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type67>(), std::declval<__type53>()))>::type __type68;
      typedef decltype(pythonic::operator_::sub(std::declval<__type42>(), std::declval<__type68>())) __type69;
      typedef decltype(pythonic::operator_::mul(std::declval<__type69>(), std::declval<__type63>())) __type70;
      typedef container<typename std::remove_reference<__type70>::type> __type71;
      typedef typename __combined<__type65,__type71>::type __type72;
      typedef decltype(pythonic::operator_::mul(std::declval<__type68>(), std::declval<__type63>())) __type73;
      typedef container<typename std::remove_reference<__type73>::type> __type74;
      typedef __type1 __ptype30;
      typedef __type3 __ptype31;
      typedef typename pythonic::returnable<typename __combined<__type72,__type74>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type operator()(argument_type0&& spectrum_k0k1k2, argument_type1&& khs, argument_type2&& KH, argument_type3&& kzs, argument_type4&& KZ) const
    ;
  }  ;
  struct loop_spectra3d
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type0>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type3;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type2>())) __type4;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type4>::type>::type __type5;
      typedef typename pythonic::lazy<__type5>::type __type6;
      typedef decltype(std::declval<__type3>()(std::declval<__type6>())) __type7;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type4>::type>::type __type9;
      typedef typename pythonic::lazy<__type9>::type __type10;
      typedef decltype(std::declval<__type3>()(std::declval<__type10>())) __type11;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type __type12;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type4>::type>::type __type13;
      typedef typename pythonic::lazy<__type13>::type __type14;
      typedef decltype(std::declval<__type3>()(std::declval<__type14>())) __type15;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type15>::type::iterator>::value_type>::type __type16;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type8>(), std::declval<__type12>(), std::declval<__type16>())) __type17;
      typedef decltype(std::declval<__type2>()[std::declval<__type17>()]) __type18;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type19;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type20;
      typedef container<typename std::remove_reference<__type1>::type> __type21;
      typedef typename __combined<__type0,__type21>::type __type22;
      typedef typename pythonic::assignable<decltype(std::declval<__type20>()(std::declval<__type22>()))>::type __type23;
      typedef typename pythonic::assignable<decltype(std::declval<__type19>()(std::declval<__type23>()))>::type __type24;
      typedef long __type25;
      typedef decltype(pythonic::operator_::sub(std::declval<__type23>(), std::declval<__type25>())) __type26;
      typedef typename pythonic::lazy<__type26>::type __type27;
      typedef indexable<__type27> __type28;
      typedef typename __combined<__type24,__type28>::type __type29;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type30;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sqrt{})>::type>::type __type31;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type32;
      typedef decltype(std::declval<__type32>()[std::declval<__type17>()]) __type33;
      typedef typename pythonic::assignable<decltype(std::declval<__type31>()(std::declval<__type33>()))>::type __type34;
      typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type0>::type>::type>::type __type35;
      typedef decltype(pythonic::operator_::div(std::declval<__type34>(), std::declval<__type35>())) __type36;
      typedef typename pythonic::assignable<decltype(std::declval<__type30>()(std::declval<__type36>()))>::type __type37;
      typedef indexable<__type37> __type38;
      typedef typename __combined<__type29,__type38>::type __type39;
      typedef decltype(pythonic::operator_::add(std::declval<__type37>(), std::declval<__type25>())) __type40;
      typedef indexable<__type40> __type41;
      typedef typename __combined<__type39,__type41>::type __type42;
      typedef typename pythonic::assignable<decltype(std::declval<__type2>()[std::declval<__type17>()])>::type __type43;
      typedef container<typename std::remove_reference<__type43>::type> __type44;
      typedef typename __combined<__type42,__type44>::type __type45;
      typedef decltype(std::declval<__type22>()[std::declval<__type37>()]) __type46;
      typedef decltype(pythonic::operator_::sub(std::declval<__type34>(), std::declval<__type46>())) __type47;
      typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type47>(), std::declval<__type35>()))>::type __type48;
      typedef decltype(pythonic::operator_::sub(std::declval<__type25>(), std::declval<__type48>())) __type49;
      typedef decltype(pythonic::operator_::mul(std::declval<__type49>(), std::declval<__type43>())) __type50;
      typedef container<typename std::remove_reference<__type50>::type> __type51;
      typedef typename __combined<__type45,__type51>::type __type52;
      typedef decltype(pythonic::operator_::mul(std::declval<__type48>(), std::declval<__type43>())) __type53;
      typedef container<typename std::remove_reference<__type53>::type> __type54;
      typedef __type1 __ptype34;
      typedef __type18 __ptype35;
      typedef typename pythonic::returnable<typename __combined<__type52,__type54>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& spectrum_k0k1k2, argument_type1&& ks, argument_type2&& K2) const
    ;
  }  ;
  struct vector_product
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type1;
      typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type0>())) __type2;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type3;
      typedef typename pythonic::lazy<__type3>::type __type4;
      typedef decltype(std::declval<__type1>()(std::declval<__type4>())) __type5;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type __type6;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type7;
      typedef typename pythonic::lazy<__type7>::type __type8;
      typedef decltype(std::declval<__type1>()(std::declval<__type8>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type2>::type>::type __type11;
      typedef typename pythonic::lazy<__type11>::type __type12;
      typedef decltype(std::declval<__type1>()(std::declval<__type12>())) __type13;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type13>::type::iterator>::value_type>::type __type14;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type6>(), std::declval<__type10>(), std::declval<__type14>())) __type15;
      typedef decltype(std::declval<__type0>()[std::declval<__type15>()]) __type16;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type17;
      typedef decltype(std::declval<__type17>()[std::declval<__type15>()]) __type18;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type19;
      typedef decltype(std::declval<__type19>()[std::declval<__type15>()]) __type20;
      typedef container<typename std::remove_reference<__type20>::type> __type21;
      typedef typename __combined<__type19,__type21>::type __type22;
      typedef typename pythonic::assignable<decltype(std::declval<__type17>()[std::declval<__type15>()])>::type __type23;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type24;
      typedef typename pythonic::assignable<decltype(std::declval<__type24>()[std::declval<__type15>()])>::type __type25;
      typedef decltype(pythonic::operator_::mul(std::declval<__type23>(), std::declval<__type25>())) __type26;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type27;
      typedef typename pythonic::assignable<decltype(std::declval<__type27>()[std::declval<__type15>()])>::type __type28;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type29;
      typedef typename pythonic::assignable<decltype(std::declval<__type29>()[std::declval<__type15>()])>::type __type30;
      typedef decltype(pythonic::operator_::mul(std::declval<__type28>(), std::declval<__type30>())) __type31;
      typedef decltype(pythonic::operator_::sub(std::declval<__type26>(), std::declval<__type31>())) __type32;
      typedef container<typename std::remove_reference<__type32>::type> __type33;
      typedef typename __combined<__type22,__type33>::type __type34;
      typedef indexable<__type15> __type35;
      typedef typename __combined<__type34,__type35>::type __type36;
      typedef decltype(std::declval<__type29>()[std::declval<__type15>()]) __type37;
      typedef container<typename std::remove_reference<__type37>::type> __type38;
      typedef typename __combined<__type29,__type38>::type __type39;
      typedef typename pythonic::assignable<decltype(std::declval<__type19>()[std::declval<__type15>()])>::type __type40;
      typedef decltype(pythonic::operator_::mul(std::declval<__type28>(), std::declval<__type40>())) __type41;
      typedef typename pythonic::assignable<decltype(std::declval<__type0>()[std::declval<__type15>()])>::type __type42;
      typedef decltype(pythonic::operator_::mul(std::declval<__type42>(), std::declval<__type25>())) __type43;
      typedef decltype(pythonic::operator_::sub(std::declval<__type41>(), std::declval<__type43>())) __type44;
      typedef container<typename std::remove_reference<__type44>::type> __type45;
      typedef typename __combined<__type39,__type45>::type __type46;
      typedef typename __combined<__type46,__type35>::type __type47;
      typedef decltype(std::declval<__type24>()[std::declval<__type15>()]) __type48;
      typedef container<typename std::remove_reference<__type48>::type> __type49;
      typedef typename __combined<__type24,__type49>::type __type50;
      typedef decltype(pythonic::operator_::mul(std::declval<__type42>(), std::declval<__type30>())) __type51;
      typedef decltype(pythonic::operator_::mul(std::declval<__type23>(), std::declval<__type40>())) __type52;
      typedef decltype(pythonic::operator_::sub(std::declval<__type51>(), std::declval<__type52>())) __type53;
      typedef container<typename std::remove_reference<__type53>::type> __type54;
      typedef typename __combined<__type50,__type54>::type __type55;
      typedef typename __combined<__type55,__type35>::type __type56;
      typedef __type16 __ptype36;
      typedef __type18 __ptype37;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type36>(), std::declval<__type47>(), std::declval<__type56>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& ax, argument_type1&& ay, argument_type2&& az, argument_type3&& bx, argument_type4&& by, argument_type5&& bz) const
    ;
  }  ;
  typename __transonic__::type::result_type __transonic__::operator()() const
  {
    {
      static typename __transonic__::type::result_type tmp_global = pythonic::types::make_tuple(pythonic::types::str("0.4.5"));
      return tmp_global;
    }
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft::type::result_type __code_new_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, vx_fft, vy_fft):\n"
"    return backend_func(self.Kx, self.Ky, vx_fft, vy_fft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename __for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type __for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& vx_fft, argument_type3&& vy_fft) const
  {
    return pythonic::operator_::mul(std::complex<double>(0.0, 1.0), pythonic::operator_::sub(pythonic::operator_::mul(self_Kx, vy_fft), pythonic::operator_::mul(self_Ky, vx_fft)));
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin::type::result_type __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, vx_fft, vy_fft, vz_fft, rotxfft, rotyfft, rotzfft):\n"
"    return backend_func(self.Kx, self.Ky, self.Kz, vx_fft, vy_fft, vz_fft, rotxfft, rotyfft, rotzfft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 , typename argument_type7 , typename argument_type8 >
  typename __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6, argument_type7, argument_type8>::result_type __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& vx_fft, argument_type4&& vy_fft, argument_type5&& vz_fft, argument_type6&& rotxfft, argument_type7&& rotyfft, argument_type8&& rotzfft) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type1;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type2;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type2>::type>::type __type3;
    typedef typename pythonic::lazy<__type3>::type __type4;
    typedef decltype(std::declval<__type0>()(std::declval<__type4>())) __type5;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type6;
    typedef typename pythonic::lazy<__type6>::type __type7;
    typedef decltype(std::declval<__type0>()(std::declval<__type7>())) __type8;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef decltype(std::declval<__type0>()(std::declval<__type10>())) __type11;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type>::type i2;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type>::type i1;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type>::type i0;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft)))>::type n0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft)))>::type n1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft)))>::type n2 = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft));
    {
      long  __target140506414598560 = n0;
      for (long  i0=0L; i0 < __target140506414598560; i0 += 1L)
      {
        {
          long  __target140506414600048 = n1;
          for (long  i1=0L; i1 < __target140506414600048; i1 += 1L)
          {
            {
              long  __target140506414617264 = n2;
              for (long  i2=0L; i2 < __target140506414617264; i2 += 1L)
              {
                rotxfft.fast(pythonic::types::make_tuple(i0, i1, i2)) = pythonic::operator_::mul(std::complex<double>(0.0, 1.0), pythonic::operator_::sub(pythonic::operator_::mul(self_Ky.fast(pythonic::types::make_tuple(i0, i1, i2)), vz_fft.fast(pythonic::types::make_tuple(i0, i1, i2))), pythonic::operator_::mul(self_Kz.fast(pythonic::types::make_tuple(i0, i1, i2)), vy_fft.fast(pythonic::types::make_tuple(i0, i1, i2)))));
                rotyfft.fast(pythonic::types::make_tuple(i0, i1, i2)) = pythonic::operator_::mul(std::complex<double>(0.0, 1.0), pythonic::operator_::sub(pythonic::operator_::mul(self_Kz.fast(pythonic::types::make_tuple(i0, i1, i2)), vx_fft.fast(pythonic::types::make_tuple(i0, i1, i2))), pythonic::operator_::mul(self_Kx.fast(pythonic::types::make_tuple(i0, i1, i2)), vz_fft.fast(pythonic::types::make_tuple(i0, i1, i2)))));
                rotzfft.fast(pythonic::types::make_tuple(i0, i1, i2)) = pythonic::operator_::mul(std::complex<double>(0.0, 1.0), pythonic::operator_::sub(pythonic::operator_::mul(self_Kx.fast(pythonic::types::make_tuple(i0, i1, i2)), vy_fft.fast(pythonic::types::make_tuple(i0, i1, i2))), pythonic::operator_::mul(self_Ky.fast(pythonic::types::make_tuple(i0, i1, i2)), vx_fft.fast(pythonic::types::make_tuple(i0, i1, i2)))));
              }
            }
          }
        }
      }
    }
    return pythonic::builtins::None;
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft::type::result_type __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, vx_fft, vy_fft, vz_fft):\n"
"    return backend_func(self.Kx, self.Ky, self.Kz, vx_fft, vy_fft, vz_fft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  typename __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& vx_fft, argument_type4&& vy_fft, argument_type5&& vz_fft) const
  {
    return pythonic::types::make_tuple(pythonic::operator_::mul(std::complex<double>(0.0, 1.0), pythonic::operator_::sub(pythonic::operator_::mul(self_Ky, vz_fft), pythonic::operator_::mul(self_Kz, vy_fft))), pythonic::operator_::mul(std::complex<double>(0.0, 1.0), pythonic::operator_::sub(pythonic::operator_::mul(self_Kz, vx_fft), pythonic::operator_::mul(self_Kx, vz_fft))), pythonic::operator_::mul(std::complex<double>(0.0, 1.0), pythonic::operator_::sub(pythonic::operator_::mul(self_Kx, vy_fft), pythonic::operator_::mul(self_Ky, vx_fft))));
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__divfft_from_vecfft::type::result_type __code_new_method__OperatorsPseudoSpectral3D__divfft_from_vecfft::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__divfft_from_vecfft::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, vx_fft, vy_fft, vz_fft):\n"
"    return backend_func(self.Kx, self.Ky, self.Kz, vx_fft, vy_fft, vz_fft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  typename __for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type __for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& vx_fft, argument_type4&& vy_fft, argument_type5&& vz_fft) const
  {
    return pythonic::operator_::mul(std::complex<double>(0.0, 1.0), pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::mul(self_Kx, vx_fft), pythonic::operator_::mul(self_Ky, vy_fft)), pythonic::operator_::mul(self_Kz, vz_fft)));
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d::type::result_type __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, vx_fft, vy_fft, vz_fft):\n"
"    return backend_func(self.Kx, self.Ky, self.Kz, self.inv_K_square_nozero, vx_fft, vy_fft, vz_fft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 >
  typename __for_method__OperatorsPseudoSpectral3D__project_perpk3d::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6>::result_type __for_method__OperatorsPseudoSpectral3D__project_perpk3d::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& self_inv_K_square_nozero, argument_type4&& vx_fft, argument_type5&& vy_fft, argument_type6&& vz_fft) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type1;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type2;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type2>::type>::type __type3;
    typedef typename pythonic::lazy<__type3>::type __type4;
    typedef decltype(std::declval<__type0>()(std::declval<__type4>())) __type5;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type6;
    typedef typename pythonic::lazy<__type6>::type __type7;
    typedef decltype(std::declval<__type0>()(std::declval<__type7>())) __type8;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef decltype(std::declval<__type0>()(std::declval<__type10>())) __type11;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type>::type i2;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type>::type i1;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type>::type i0;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft)))>::type n0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft)))>::type n1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft)))>::type n2 = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, vx_fft));
    {
      long  __target140506411601200 = n0;
      for (long  i0=0L; i0 < __target140506411601200; i0 += 1L)
      {
        {
          long  __target140506409272128 = n1;
          for (long  i1=0L; i1 < __target140506409272128; i1 += 1L)
          {
            {
              long  __target140506409272848 = n2;
              for (long  i2=0L; i2 < __target140506409272848; i2 += 1L)
              {
                typename pythonic::assignable<decltype(pythonic::operator_::mul(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::mul(self_Kx.fast(pythonic::types::make_tuple(i0, i1, i2)), vx_fft.fast(pythonic::types::make_tuple(i0, i1, i2))), pythonic::operator_::mul(self_Ky.fast(pythonic::types::make_tuple(i0, i1, i2)), vy_fft.fast(pythonic::types::make_tuple(i0, i1, i2)))), pythonic::operator_::mul(self_Kz.fast(pythonic::types::make_tuple(i0, i1, i2)), vz_fft.fast(pythonic::types::make_tuple(i0, i1, i2)))), self_inv_K_square_nozero.fast(pythonic::types::make_tuple(i0, i1, i2))))>::type tmp = pythonic::operator_::mul(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::mul(self_Kx.fast(pythonic::types::make_tuple(i0, i1, i2)), vx_fft.fast(pythonic::types::make_tuple(i0, i1, i2))), pythonic::operator_::mul(self_Ky.fast(pythonic::types::make_tuple(i0, i1, i2)), vy_fft.fast(pythonic::types::make_tuple(i0, i1, i2)))), pythonic::operator_::mul(self_Kz.fast(pythonic::types::make_tuple(i0, i1, i2)), vz_fft.fast(pythonic::types::make_tuple(i0, i1, i2)))), self_inv_K_square_nozero.fast(pythonic::types::make_tuple(i0, i1, i2)));
                vx_fft.fast(pythonic::types::make_tuple(i0, i1, i2)) -= pythonic::operator_::mul(self_Kx.fast(pythonic::types::make_tuple(i0, i1, i2)), tmp);
                vy_fft.fast(pythonic::types::make_tuple(i0, i1, i2)) -= pythonic::operator_::mul(self_Ky.fast(pythonic::types::make_tuple(i0, i1, i2)), tmp);
                vz_fft.fast(pythonic::types::make_tuple(i0, i1, i2)) -= pythonic::operator_::mul(self_Kz.fast(pythonic::types::make_tuple(i0, i1, i2)), tmp);
              }
            }
          }
        }
      }
    }
    return pythonic::builtins::None;
  }
  typename __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop::type::result_type __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop::operator()() const
  {
    {
      static typename __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop::type::result_type tmp_global = pythonic::types::str("\n"
"\n"
"def new_method(self, vx_fft, vy_fft, vz_fft):\n"
"    return backend_func(self.Kx, self.Ky, self.Kz, self.inv_K_square_nozero, vx_fft, vy_fft, vz_fft)\n"
"\n"
"");
      return tmp_global;
    }
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 >
  typename __for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6>::result_type __for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop::operator()(argument_type0&& self_Kx, argument_type1&& self_Ky, argument_type2&& self_Kz, argument_type3&& self_inv_K_square_nozero, argument_type4&& vx_fft, argument_type5&& vy_fft, argument_type6&& vz_fft) const
  {
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type6>::type>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type>::type __type3;
    typedef decltype(pythonic::operator_::mul(std::declval<__type2>(), std::declval<__type3>())) __type4;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type5;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type>::type __type6;
    typedef decltype(pythonic::operator_::mul(std::declval<__type5>(), std::declval<__type6>())) __type7;
    typedef decltype(pythonic::operator_::add(std::declval<__type4>(), std::declval<__type7>())) __type8;
    typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type0>())) __type9;
    typedef decltype(pythonic::operator_::add(std::declval<__type8>(), std::declval<__type9>())) __type10;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type11;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::mul(std::declval<__type10>(), std::declval<__type11>()))>::type __type12;
    typedef decltype(pythonic::operator_::mul(std::declval<__type1>(), std::declval<__type12>())) __type13;
    typedef decltype(pythonic::operator_::mul(std::declval<__type5>(), std::declval<__type12>())) __type14;
    typedef decltype(pythonic::operator_::mul(std::declval<__type2>(), std::declval<__type12>())) __type15;
    typename pythonic::assignable<typename __combined<__type0,__type13>::type>::type vz_fft_ = vz_fft;
    typename pythonic::assignable<typename __combined<__type6,__type14>::type>::type vy_fft_ = vy_fft;
    typename pythonic::assignable<typename __combined<__type3,__type15>::type>::type vx_fft_ = vx_fft;
    typename pythonic::assignable<decltype(pythonic::operator_::mul(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::mul(self_Kx, vx_fft_), pythonic::operator_::mul(self_Ky, vy_fft_)), pythonic::operator_::mul(self_Kz, vz_fft_)), self_inv_K_square_nozero))>::type tmp = pythonic::operator_::mul(pythonic::operator_::add(pythonic::operator_::add(pythonic::operator_::mul(self_Kx, vx_fft_), pythonic::operator_::mul(self_Ky, vy_fft_)), pythonic::operator_::mul(self_Kz, vz_fft_)), self_inv_K_square_nozero);
    vx_fft_ -= pythonic::operator_::mul(self_Kx, tmp);
    vy_fft_ -= pythonic::operator_::mul(self_Ky, tmp);
    vz_fft_ -= pythonic::operator_::mul(self_Kz, tmp);
    return pythonic::builtins::None;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
  typename loop_spectra_kzkh::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type loop_spectra_kzkh::operator()(argument_type0&& spectrum_k0k1k2, argument_type1&& khs, argument_type2&& KH, argument_type3&& kzs, argument_type4&& KZ) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::pythran::functor::make_shape{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type3;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type __type4;
    typedef container<typename std::remove_reference<__type4>::type> __type5;
    typedef typename __combined<__type3,__type5>::type __type6;
    typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type6>()))>::type __type7;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type8;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type8>::type>::type __type9;
    typedef container<typename std::remove_reference<__type9>::type> __type10;
    typedef typename __combined<__type8,__type10>::type __type11;
    typedef typename pythonic::assignable<decltype(std::declval<__type2>()(std::declval<__type11>()))>::type __type12;
    typedef decltype(std::declval<__type1>()(std::declval<__type7>(), std::declval<__type12>())) __type13;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type13>()))>::type __type14;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type15;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::round{})>::type>::type __type16;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::abs{})>::type>::type __type17;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type18;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type19;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type20;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type20>())) __type21;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type21>::type>::type __type22;
    typedef typename pythonic::lazy<__type22>::type __type23;
    typedef decltype(std::declval<__type19>()(std::declval<__type23>())) __type24;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type24>::type::iterator>::value_type>::type __type25;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type21>::type>::type __type26;
    typedef typename pythonic::lazy<__type26>::type __type27;
    typedef decltype(std::declval<__type19>()(std::declval<__type27>())) __type28;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type28>::type::iterator>::value_type>::type __type29;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type21>::type>::type __type30;
    typedef typename pythonic::lazy<__type30>::type __type31;
    typedef decltype(std::declval<__type19>()(std::declval<__type31>())) __type32;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type32>::type::iterator>::value_type>::type __type33;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type25>(), std::declval<__type29>(), std::declval<__type33>())) __type34;
    typedef decltype(std::declval<__type18>()[std::declval<__type34>()]) __type35;
    typedef decltype(std::declval<__type17>()(std::declval<__type35>())) __type36;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type>::type __type37;
    typedef decltype(pythonic::operator_::div(std::declval<__type36>(), std::declval<__type37>())) __type38;
    typedef decltype(std::declval<__type16>()(std::declval<__type38>())) __type39;
    typedef decltype(std::declval<__type15>()(std::declval<__type39>())) __type40;
    typedef typename pythonic::lazy<__type40>::type __type41;
    typedef long __type42;
    typedef decltype(pythonic::operator_::sub(std::declval<__type7>(), std::declval<__type42>())) __type43;
    typedef typename pythonic::lazy<__type43>::type __type44;
    typedef typename __combined<__type41,__type44>::type __type45;
    typedef decltype(pythonic::operator_::sub(std::declval<__type12>(), std::declval<__type42>())) __type46;
    typedef typename pythonic::lazy<__type46>::type __type47;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type45>(), std::declval<__type47>())) __type48;
    typedef indexable<__type48> __type49;
    typedef typename __combined<__type14,__type49>::type __type50;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type51;
    typedef typename pythonic::assignable<decltype(std::declval<__type51>()[std::declval<__type34>()])>::type __type52;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type8>::type>::type>::type __type53;
    typedef decltype(pythonic::operator_::div(std::declval<__type52>(), std::declval<__type53>())) __type54;
    typedef typename pythonic::assignable<decltype(std::declval<__type15>()(std::declval<__type54>()))>::type __type55;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type45>(), std::declval<__type55>())) __type56;
    typedef indexable<__type56> __type57;
    typedef typename __combined<__type50,__type57>::type __type58;
    typedef decltype(pythonic::operator_::add(std::declval<__type55>(), std::declval<__type42>())) __type59;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type45>(), std::declval<__type59>())) __type60;
    typedef indexable<__type60> __type61;
    typedef typename __combined<__type58,__type61>::type __type62;
    typedef typename __combined<__type62,__type49>::type __type63;
    typedef typename pythonic::assignable<decltype(std::declval<__type20>()[std::declval<__type34>()])>::type __type64;
    typedef container<typename std::remove_reference<__type64>::type> __type65;
    typedef typename __combined<__type63,__type65>::type __type66;
    typedef typename __combined<__type66,__type57>::type __type67;
    typedef decltype(std::declval<__type11>()[std::declval<__type55>()]) __type68;
    typedef decltype(pythonic::operator_::sub(std::declval<__type52>(), std::declval<__type68>())) __type69;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type69>(), std::declval<__type53>()))>::type __type70;
    typedef decltype(pythonic::operator_::sub(std::declval<__type42>(), std::declval<__type70>())) __type71;
    typedef decltype(pythonic::operator_::mul(std::declval<__type71>(), std::declval<__type64>())) __type72;
    typedef container<typename std::remove_reference<__type72>::type> __type73;
    typedef typename __combined<__type67,__type73>::type __type74;
    typedef typename __combined<__type74,__type61>::type __type75;
    typedef decltype(pythonic::operator_::mul(std::declval<__type70>(), std::declval<__type64>())) __type76;
    typedef container<typename std::remove_reference<__type76>::type> __type77;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type32>::type::iterator>::value_type>::type>::type ik2;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type28>::type::iterator>::value_type>::type>::type ik1;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type24>::type::iterator>::value_type>::type>::type ik0;
    typename pythonic::assignable<decltype(std::get<1>(khs))>::type deltakh = std::get<1>(khs);
    typename pythonic::assignable<decltype(std::get<1>(kzs))>::type deltakz = std::get<1>(kzs);
    typename pythonic::assignable<decltype(pythonic::builtins::functor::len{}(khs))>::type nkh = pythonic::builtins::functor::len{}(khs);
    typename pythonic::assignable<decltype(pythonic::builtins::functor::len{}(kzs))>::type nkz = pythonic::builtins::functor::len{}(kzs);
    typename pythonic::assignable<typename __combined<__type75,__type77>::type>::type spectrum_kzkh = pythonic::numpy::functor::zeros{}(pythonic::builtins::pythran::functor::make_shape{}(nkz, nkh));
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2)))>::type nk0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2)))>::type nk1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2)))>::type nk2 = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2));
    {
      long  __target140506409180320 = nk0;
      for (long  ik0=0L; ik0 < __target140506409180320; ik0 += 1L)
      {
        {
          long  __target140506409187408 = nk1;
          for (long  ik1=0L; ik1 < __target140506409187408; ik1 += 1L)
          {
            {
              long  __target140506409188176 = nk2;
              for (long  ik2=0L; ik2 < __target140506409188176; ik2 += 1L)
              {
                typename pythonic::assignable<decltype(spectrum_k0k1k2.fast(pythonic::types::make_tuple(ik0, ik1, ik2)))>::type value = spectrum_k0k1k2.fast(pythonic::types::make_tuple(ik0, ik1, ik2));
                typename pythonic::assignable<decltype(KH.fast(pythonic::types::make_tuple(ik0, ik1, ik2)))>::type kappa = KH.fast(pythonic::types::make_tuple(ik0, ik1, ik2));
                typename pythonic::assignable<decltype(pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltakh)))>::type ikh = pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltakh));
                typename pythonic::lazy<__type45>::type ikz = pythonic::builtins::functor::int_{}(pythonic::builtins::functor::round{}(pythonic::operator_::div(pythonic::builtins::functor::abs{}(KZ.fast(pythonic::types::make_tuple(ik0, ik1, ik2))), deltakz)));
                if (pythonic::operator_::ge(ikz, pythonic::operator_::sub(nkz, 1L)))
                {
                  ikz = pythonic::operator_::sub(nkz, 1L);
                }
                {
                  typename pythonic::assignable<typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type69>(), std::declval<__type53>()))>::type>::type coef_share;
                  if (pythonic::operator_::ge(ikh, pythonic::operator_::sub(nkh, 1L)))
                  {
                    typename pythonic::lazy<decltype(pythonic::operator_::sub(nkh, 1L))>::type ikh_ = pythonic::operator_::sub(nkh, 1L);
                    spectrum_kzkh[pythonic::types::make_tuple(ikz, ikh_)] += value;
                  }
                  else
                  {
                    coef_share = pythonic::operator_::div(pythonic::operator_::sub(kappa, khs[ikh]), deltakh);
                    spectrum_kzkh[pythonic::types::make_tuple(ikz, ikh)] += pythonic::operator_::mul(pythonic::operator_::sub(1L, coef_share), value);
                    spectrum_kzkh[pythonic::types::make_tuple(ikz, pythonic::operator_::add(ikh, 1L))] += pythonic::operator_::mul(coef_share, value);
                  }
                }
              }
            }
          }
        }
      }
    }
    return spectrum_kzkh;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename loop_spectra3d::type<argument_type0, argument_type1, argument_type2>::result_type loop_spectra3d::operator()(argument_type0&& spectrum_k0k1k2, argument_type1&& ks, argument_type2&& K2) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::len{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type3;
    typedef container<typename std::remove_reference<__type3>::type> __type4;
    typedef typename __combined<__type2,__type4>::type __type5;
    typedef typename pythonic::assignable<decltype(std::declval<__type1>()(std::declval<__type5>()))>::type __type6;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type6>()))>::type __type7;
    typedef long __type8;
    typedef decltype(pythonic::operator_::sub(std::declval<__type6>(), std::declval<__type8>())) __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef indexable<__type10> __type11;
    typedef typename __combined<__type7,__type11>::type __type12;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::int_{})>::type>::type __type13;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sqrt{})>::type>::type __type14;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type15;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type16;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type17;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type17>())) __type18;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type18>::type>::type __type19;
    typedef typename pythonic::lazy<__type19>::type __type20;
    typedef decltype(std::declval<__type16>()(std::declval<__type20>())) __type21;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type21>::type::iterator>::value_type>::type __type22;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type18>::type>::type __type23;
    typedef typename pythonic::lazy<__type23>::type __type24;
    typedef decltype(std::declval<__type16>()(std::declval<__type24>())) __type25;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type25>::type::iterator>::value_type>::type __type26;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type18>::type>::type __type27;
    typedef typename pythonic::lazy<__type27>::type __type28;
    typedef decltype(std::declval<__type16>()(std::declval<__type28>())) __type29;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type29>::type::iterator>::value_type>::type __type30;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type22>(), std::declval<__type26>(), std::declval<__type30>())) __type31;
    typedef decltype(std::declval<__type15>()[std::declval<__type31>()]) __type32;
    typedef typename pythonic::assignable<decltype(std::declval<__type14>()(std::declval<__type32>()))>::type __type33;
    typedef typename pythonic::assignable<typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type>::type __type34;
    typedef decltype(pythonic::operator_::div(std::declval<__type33>(), std::declval<__type34>())) __type35;
    typedef typename pythonic::assignable<decltype(std::declval<__type13>()(std::declval<__type35>()))>::type __type36;
    typedef indexable<__type36> __type37;
    typedef typename __combined<__type12,__type37>::type __type38;
    typedef decltype(pythonic::operator_::add(std::declval<__type36>(), std::declval<__type8>())) __type39;
    typedef indexable<__type39> __type40;
    typedef typename __combined<__type38,__type40>::type __type41;
    typedef typename __combined<__type41,__type11>::type __type42;
    typedef typename pythonic::assignable<decltype(std::declval<__type17>()[std::declval<__type31>()])>::type __type43;
    typedef container<typename std::remove_reference<__type43>::type> __type44;
    typedef typename __combined<__type42,__type44>::type __type45;
    typedef typename __combined<__type45,__type37>::type __type46;
    typedef decltype(std::declval<__type5>()[std::declval<__type36>()]) __type47;
    typedef decltype(pythonic::operator_::sub(std::declval<__type33>(), std::declval<__type47>())) __type48;
    typedef typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type48>(), std::declval<__type34>()))>::type __type49;
    typedef decltype(pythonic::operator_::sub(std::declval<__type8>(), std::declval<__type49>())) __type50;
    typedef decltype(pythonic::operator_::mul(std::declval<__type50>(), std::declval<__type43>())) __type51;
    typedef container<typename std::remove_reference<__type51>::type> __type52;
    typedef typename __combined<__type46,__type52>::type __type53;
    typedef typename __combined<__type53,__type40>::type __type54;
    typedef decltype(pythonic::operator_::mul(std::declval<__type49>(), std::declval<__type43>())) __type55;
    typedef container<typename std::remove_reference<__type55>::type> __type56;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type29>::type::iterator>::value_type>::type>::type ik2;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type25>::type::iterator>::value_type>::type>::type ik1;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type21>::type::iterator>::value_type>::type>::type ik0;
    typename pythonic::assignable<decltype(std::get<1>(ks))>::type deltak = std::get<1>(ks);
    typename pythonic::assignable<decltype(pythonic::builtins::functor::len{}(ks))>::type nk = pythonic::builtins::functor::len{}(ks);
    typename pythonic::assignable<typename __combined<__type54,__type56>::type>::type spectrum3d = pythonic::numpy::functor::zeros{}(nk);
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2)))>::type nk0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2)))>::type nk1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2)))>::type nk2 = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, spectrum_k0k1k2));
    {
      long  __target140506411507088 = nk0;
      for (long  ik0=0L; ik0 < __target140506411507088; ik0 += 1L)
      {
        {
          long  __target140506409142160 = nk1;
          for (long  ik1=0L; ik1 < __target140506409142160; ik1 += 1L)
          {
            {
              long  __target140506409142880 = nk2;
              for (long  ik2=0L; ik2 < __target140506409142880; ik2 += 1L)
              {
                typename pythonic::assignable<decltype(spectrum_k0k1k2.fast(pythonic::types::make_tuple(ik0, ik1, ik2)))>::type value = spectrum_k0k1k2.fast(pythonic::types::make_tuple(ik0, ik1, ik2));
                typename pythonic::assignable<decltype(pythonic::numpy::functor::sqrt{}(K2.fast(pythonic::types::make_tuple(ik0, ik1, ik2))))>::type kappa = pythonic::numpy::functor::sqrt{}(K2.fast(pythonic::types::make_tuple(ik0, ik1, ik2)));
                typename pythonic::assignable<decltype(pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltak)))>::type ik = pythonic::builtins::functor::int_{}(pythonic::operator_::div(kappa, deltak));
                {
                  typename pythonic::assignable<typename pythonic::assignable<decltype(pythonic::operator_::div(std::declval<__type48>(), std::declval<__type34>()))>::type>::type coef_share;
                  if (pythonic::operator_::ge(ik, pythonic::operator_::sub(nk, 1L)))
                  {
                    typename pythonic::lazy<decltype(pythonic::operator_::sub(nk, 1L))>::type ik_ = pythonic::operator_::sub(nk, 1L);
                    spectrum3d[ik_] += value;
                  }
                  else
                  {
                    coef_share = pythonic::operator_::div(pythonic::operator_::sub(kappa, ks[ik]), deltak);
                    spectrum3d[ik] += pythonic::operator_::mul(pythonic::operator_::sub(1L, coef_share), value);
                    spectrum3d[pythonic::operator_::add(ik, 1L)] += pythonic::operator_::mul(coef_share, value);
                  }
                }
              }
            }
          }
        }
      }
    }
    return spectrum3d;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  typename vector_product::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type vector_product::operator()(argument_type0&& ax, argument_type1&& ay, argument_type2&& az, argument_type3&& bx, argument_type4&& by, argument_type5&& bz) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::builtins::functor::range{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type1;
    typedef decltype(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, std::declval<__type1>())) __type2;
    typedef typename std::tuple_element<2,typename std::remove_reference<__type2>::type>::type __type3;
    typedef typename pythonic::lazy<__type3>::type __type4;
    typedef decltype(std::declval<__type0>()(std::declval<__type4>())) __type5;
    typedef typename std::tuple_element<1,typename std::remove_reference<__type2>::type>::type __type6;
    typedef typename pythonic::lazy<__type6>::type __type7;
    typedef decltype(std::declval<__type0>()(std::declval<__type7>())) __type8;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type9;
    typedef typename pythonic::lazy<__type9>::type __type10;
    typedef decltype(std::declval<__type0>()(std::declval<__type10>())) __type11;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type>::type i2;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type8>::type::iterator>::value_type>::type>::type i1;
    typename pythonic::assignable<typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type11>::type::iterator>::value_type>::type>::type i0;
    typename pythonic::lazy<decltype(std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ax)))>::type n0 = std::get<0>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ax));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ax)))>::type n1 = std::get<1>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ax));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ax)))>::type n2 = std::get<2>(pythonic::builtins::getattr(pythonic::types::attr::SHAPE{}, ax));
    {
      long  __target140506411620384 = n0;
      for (long  i0=0L; i0 < __target140506411620384; i0 += 1L)
      {
        {
          long  __target140506411621920 = n1;
          for (long  i1=0L; i1 < __target140506411621920; i1 += 1L)
          {
            {
              long  __target140506411622656 = n2;
              for (long  i2=0L; i2 < __target140506411622656; i2 += 1L)
              {
                typename pythonic::assignable<decltype(ax.fast(pythonic::types::make_tuple(i0, i1, i2)))>::type elem_ax = ax.fast(pythonic::types::make_tuple(i0, i1, i2));
                typename pythonic::assignable<decltype(ay.fast(pythonic::types::make_tuple(i0, i1, i2)))>::type elem_ay = ay.fast(pythonic::types::make_tuple(i0, i1, i2));
                typename pythonic::assignable<decltype(az.fast(pythonic::types::make_tuple(i0, i1, i2)))>::type elem_az = az.fast(pythonic::types::make_tuple(i0, i1, i2));
                typename pythonic::assignable<decltype(bx.fast(pythonic::types::make_tuple(i0, i1, i2)))>::type elem_bx = bx.fast(pythonic::types::make_tuple(i0, i1, i2));
                typename pythonic::assignable<decltype(by.fast(pythonic::types::make_tuple(i0, i1, i2)))>::type elem_by = by.fast(pythonic::types::make_tuple(i0, i1, i2));
                typename pythonic::assignable<decltype(bz.fast(pythonic::types::make_tuple(i0, i1, i2)))>::type elem_bz = bz.fast(pythonic::types::make_tuple(i0, i1, i2));
                bx.fast(pythonic::types::make_tuple(i0, i1, i2)) = pythonic::operator_::sub(pythonic::operator_::mul(elem_ay, elem_bz), pythonic::operator_::mul(elem_az, elem_by));
                by.fast(pythonic::types::make_tuple(i0, i1, i2)) = pythonic::operator_::sub(pythonic::operator_::mul(elem_az, elem_bx), pythonic::operator_::mul(elem_ax, elem_bz));
                bz.fast(pythonic::types::make_tuple(i0, i1, i2)) = pythonic::operator_::sub(pythonic::operator_::mul(elem_ax, elem_by), pythonic::operator_::mul(elem_ay, elem_bx));
              }
            }
          }
        }
      }
    }
    return pythonic::types::make_tuple(bx, by, bz);
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
static PyObject* __transonic__ = to_python(__pythran_operators::__transonic__()());
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft = to_python(__pythran_operators::__code_new_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft()());
typename __pythran_operators::__for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft()(self_Kx, self_Ky, vx_fft, vy_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin = to_python(__pythran_operators::__code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin()());
typename __pythran_operators::__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kz, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vz_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& rotxfft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& rotyfft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& rotzfft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin()(self_Kx, self_Ky, self_Kz, vx_fft, vy_fft, vz_fft, rotxfft, rotyfft, rotzfft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft = to_python(__pythran_operators::__code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft()());
typename __pythran_operators::__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kz, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vz_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft()(self_Kx, self_Ky, self_Kz, vx_fft, vy_fft, vz_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__divfft_from_vecfft = to_python(__pythran_operators::__code_new_method__OperatorsPseudoSpectral3D__divfft_from_vecfft()());
typename __pythran_operators::__for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kz, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vz_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft()(self_Kx, self_Ky, self_Kz, vx_fft, vy_fft, vz_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d = to_python(__pythran_operators::__code_new_method__OperatorsPseudoSpectral3D__project_perpk3d()());
typename __pythran_operators::__for_method__OperatorsPseudoSpectral3D__project_perpk3d::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__project_perpk3d0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kz, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_inv_K_square_nozero, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& vy_fft, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& vz_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsPseudoSpectral3D__project_perpk3d()(self_Kx, self_Ky, self_Kz, self_inv_K_square_nozero, vx_fft, vy_fft, vz_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsPseudoSpectral3D__project_perpk3d::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__project_perpk3d1(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kz, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_inv_K_square_nozero, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vz_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsPseudoSpectral3D__project_perpk3d()(self_Kx, self_Ky, self_Kz, self_inv_K_square_nozero, vx_fft, vy_fft, vz_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
static PyObject* __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop = to_python(__pythran_operators::__code_new_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop()());
typename __pythran_operators::__for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kz, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_inv_K_square_nozero, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& vy_fft, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& vz_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop()(self_Kx, self_Ky, self_Kz, self_inv_K_square_nozero, vx_fft, vy_fft, vz_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::__for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>::result_type __for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop1(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Ky, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_Kz, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& self_inv_K_square_nozero, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vx_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vy_fft, pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>&& vz_fft) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::__for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop()(self_Kx, self_Ky, self_Kz, self_inv_K_square_nozero, vx_fft, vy_fft, vz_fft);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::loop_spectra_kzkh::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>::result_type loop_spectra_kzkh0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& spectrum_k0k1k2, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& khs, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& KH, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& kzs, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& KZ) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::loop_spectra_kzkh()(spectrum_k0k1k2, khs, KH, kzs, KZ);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::loop_spectra3d::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>::result_type loop_spectra3d0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& spectrum_k0k1k2, pythonic::types::ndarray<double,pythonic::types::pshape<long>>&& ks, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::loop_spectra3d()(spectrum_k0k1k2, ks, K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_operators::vector_product::type<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>::result_type vector_product0(pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& ax, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& ay, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& az, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& bx, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& by, pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>&& bz) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_operators::vector_product()(ax, ay, az, bx, by, bz);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "vx_fft", "vy_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[9+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "self_Kz", "vx_fft", "vy_fft", "vz_fft", "rotxfft", "rotyfft", "rotzfft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6], &args_obj[7], &args_obj[8]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[6]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[7]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[8]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[6]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[7]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[8])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "self_Kz", "vx_fft", "vy_fft", "vz_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "self_Kz", "vx_fft", "vy_fft", "vz_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__project_perpk3d0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[7+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "self_Kz", "self_inv_K_square_nozero", "vx_fft", "vy_fft", "vz_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[6]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__project_perpk3d0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[6])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__project_perpk3d1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[7+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "self_Kz", "self_inv_K_square_nozero", "vx_fft", "vy_fft", "vz_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[6]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__project_perpk3d1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[6])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[7+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "self_Kz", "self_inv_K_square_nozero", "vx_fft", "vy_fft", "vz_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[6]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[6])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap___for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[7+1];
    char const* keywords[] = {"self_Kx", "self_Ky", "self_Kz", "self_inv_K_square_nozero", "vx_fft", "vy_fft", "vz_fft",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[6]))
        return to_python(__for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop1(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[5]), from_python<pythonic::types::ndarray<std::complex<double>,pythonic::types::pshape<long,long,long>>>(args_obj[6])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_loop_spectra_kzkh0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"spectrum_k0k1k2", "khs", "KH", "kzs", "KZ",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]))
        return to_python(loop_spectra_kzkh0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_loop_spectra3d0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"spectrum_k0k1k2", "ks", "K2",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]))
        return to_python(loop_spectra3d0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vector_product0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"ax", "ay", "az", "bx", "by", "bz",  nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords , &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5]))
        return to_python(vector_product0(from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[3]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[4]), from_python<pythonic::types::ndarray<double,pythonic::types::pshape<long,long,long>>>(args_obj[5])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft", "\n""    - __for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft(float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin", "\n""    - __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin(float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft", "\n""    - __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft(float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft", "\n""    - __for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft(float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__project_perpk3d(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__project_perpk3d0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__project_perpk3d1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__project_perpk3d", "\n""    - __for_method__OperatorsPseudoSpectral3D__project_perpk3d(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:])\n""    - __for_method__OperatorsPseudoSpectral3D__project_perpk3d(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall___for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap___for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "__for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop", "\n""    - __for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:])\n""    - __for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_loop_spectra_kzkh(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_loop_spectra_kzkh0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "loop_spectra_kzkh", "\n""    - loop_spectra_kzkh(float64[:,:,:], float64[:], float64[:,:,:], float64[:], float64[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_loop_spectra3d(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_loop_spectra3d0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "loop_spectra3d", "\n""    - loop_spectra3d(float64[:,:,:], float64[:], float64[:,:,:])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_vector_product(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_vector_product0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "vector_product", "\n""    - vector_product(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "__for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the z component of the curl in spectral space.\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft(float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:])"},{
    "__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin,
    METH_VARARGS | METH_KEYWORDS,
    "Return the curl of a vector in spectral space.\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin(float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])"},{
    "__for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft,
    METH_VARARGS | METH_KEYWORDS,
    "Return the curl of a vector in spectral space.\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft(float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])"},{
    "__for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft,
    METH_VARARGS | METH_KEYWORDS,
    "Return the divergence of a vector in spectral space.\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__divfft_from_vecfft(float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])"},{
    "__for_method__OperatorsPseudoSpectral3D__project_perpk3d",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__project_perpk3d,
    METH_VARARGS | METH_KEYWORDS,
    "Project (inplace) a vector perpendicular to the wavevector.\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__project_perpk3d(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:])\n""    - __for_method__OperatorsPseudoSpectral3D__project_perpk3d(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])\n""\n""        The resulting vector is divergence-free.\n""\n"""},{
    "__for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop",
    (PyCFunction)__pythran_wrapall___for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop,
    METH_VARARGS | METH_KEYWORDS,
    "Project (inplace) a vector perpendicular to the wavevector.\n""\n""    Supported prototypes:\n""\n""    - __for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:])\n""    - __for_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], complex128[:,:,:], complex128[:,:,:], complex128[:,:,:])\n""\n""        The resulting vector is divergence-free.\n""\n"""},{
    "loop_spectra_kzkh",
    (PyCFunction)__pythran_wrapall_loop_spectra_kzkh,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the kz-kh spectrum.\n""\n""    Supported prototypes:\n""\n""    - loop_spectra_kzkh(float64[:,:,:], float64[:], float64[:,:,:], float64[:], float64[:,:,:])"},{
    "loop_spectra3d",
    (PyCFunction)__pythran_wrapall_loop_spectra3d,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the 3d spectrum.\n""\n""    Supported prototypes:\n""\n""    - loop_spectra3d(float64[:,:,:], float64[:], float64[:,:,:])"},{
    "vector_product",
    (PyCFunction)__pythran_wrapall_vector_product,
    METH_VARARGS | METH_KEYWORDS,
    "Compute the vector product.\n""\n""    Supported prototypes:\n""\n""    - vector_product(float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:], float64[:,:,:])\n""\n""    Warning: the arrays bx, by, bz are overwritten.\n""\n"""},
    {NULL, NULL, 0, NULL}
};


            #if PY_MAJOR_VERSION >= 3
              static struct PyModuleDef moduledef = {
                PyModuleDef_HEAD_INIT,
                "operators",            /* m_name */
                "",         /* m_doc */
                -1,                  /* m_size */
                Methods,             /* m_methods */
                NULL,                /* m_reload */
                NULL,                /* m_traverse */
                NULL,                /* m_clear */
                NULL,                /* m_free */
              };
            #define PYTHRAN_RETURN return theModule
            #define PYTHRAN_MODULE_INIT(s) PyInit_##s
            #else
            #define PYTHRAN_RETURN return
            #define PYTHRAN_MODULE_INIT(s) init##s
            #endif
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(operators)(void)
            #ifndef _WIN32
            __attribute__ ((visibility("default")))
            __attribute__ ((externally_visible))
            #endif
            ;
            PyMODINIT_FUNC
            PYTHRAN_MODULE_INIT(operators)(void) {
                import_array()
                #if PY_MAJOR_VERSION >= 3
                PyObject* theModule = PyModule_Create(&moduledef);
                #else
                PyObject* theModule = Py_InitModule3("operators",
                                                     Methods,
                                                     ""
                );
                #endif
                if(! theModule)
                    PYTHRAN_RETURN;
                PyObject * theDoc = Py_BuildValue("(sss)",
                                                  "0.9.5",
                                                  "2020-10-15 13:19:40.105364",
                                                  "8e07b71f93b8a789e9456e40c96acc438207cfa6e334f14ff57244bba7085fe2");
                if(! theDoc)
                    PYTHRAN_RETURN;
                PyModule_AddObject(theModule,
                                   "__pythran__",
                                   theDoc);

                PyModule_AddObject(theModule, "__transonic__", __transonic__);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft", __code_new_method__OperatorsPseudoSpectral3D__rotzfft_from_vxvyfft);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin", __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft_outin);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft", __code_new_method__OperatorsPseudoSpectral3D__rotfft_from_vecfft);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__divfft_from_vecfft", __code_new_method__OperatorsPseudoSpectral3D__divfft_from_vecfft);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__project_perpk3d", __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d);
PyModule_AddObject(theModule, "__code_new_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop", __code_new_method__OperatorsPseudoSpectral3D__project_perpk3d_noloop);
                PYTHRAN_RETURN;
            }

#endif