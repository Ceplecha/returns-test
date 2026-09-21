
TYPED_PARTIAL_FUNCTION = 'returns.curry.partial'
TYPED_CURRY_FUNCTION = 'returns.curry.curry'
TYPED_FLOW_FUNCTION = 'returns._internal.pipeline.flow.flow'
TYPED_PIPE_FUNCTION = 'returns._internal.pipeline.pipe.pipe'
TYPED_PIPE_METHOD = 'returns._internal.pipeline.pipe._Pipe.__call__'
TYPED_KINDN = 'returns.primitives.hkt.KindN'
TYPED_KINDN_ACCESS = f'{TYPED_KINDN}.'
TYPED_KIND_DEKIND = 'returns.primitives.hkt.dekind'
TYPED_KIND_KINDED_CALL = 'returns.primitives.hkt.Kinded.__call__'
TYPED_KIND_KINDED_GET = 'returns.primitives.hkt.Kinded.__get__'
DO_NOTATION_METHODS = (
    'returns.io.IO.do',
    'returns.maybe.Maybe.do',
    'returns.future.Future.do',
    'returns.result.Result.do',
    'returns.io.IOResult.do',
    'returns.future.FutureResult.do',
)
