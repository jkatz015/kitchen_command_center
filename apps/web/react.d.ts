declare module 'react' {
  export interface ReactElement<P = any, T extends string | JSXElementConstructor<any> = string | JSXElementConstructor<any>> {
    type: T;
    props: P;
    key: Key | null;
  }

  export interface ReactNode {
    type: any;
    props: any;
    key: any;
  }

  export type ReactText = string | number;
  export type ReactChild = ReactElement | ReactText;
  export type ReactFragment = {} | ReactNode[];
  export type ReactNode = ReactChild | ReactFragment | ReactPortal | boolean | null | undefined;

  export interface ReactPortal {
    children: ReactNode;
    containerInfo: any;
    implementation: any;
  }

  export interface Component<P = {}, S = {}> {
    props: P;
    state: S;
    context: any;
    refs: any;
  }

  export interface FunctionComponent<P = {}> {
    (props: P, context?: any): ReactElement<any, any> | null;
    propTypes?: any;
    contextTypes?: any;
    defaultProps?: Partial<P>;
    displayName?: string;
  }

  export interface ComponentClass<P = {}, S = any> {
    new (props: P, context?: any): Component<P, S>;
    propTypes?: any;
    contextTypes?: any;
    childContextTypes?: any;
    defaultProps?: Partial<P>;
    displayName?: string;
  }

  export type ComponentType<P = {}> = ComponentClass<P, any> | FunctionComponent<P>;
  export type Key = string | number;
  export type JSXElementConstructor<P> = ((props: P) => ReactElement<any, any> | null) | ComponentClass<P, any>;

  export function useState<S>(initialState: S | (() => S)): [S, (value: S | ((prevState: S) => S)) => void];
  export function useState<S = undefined>(): [S | undefined, (value: S | ((prevState: S | undefined) => S | undefined)) => void];
  export function useEffect(effect: () => void | (() => void), deps?: any[]): void;
  export function useCallback<T extends (...args: any[]) => any>(callback: T, deps: any[]): T;
  export function useMemo<T>(factory: () => T, deps: any[] | undefined | null): T;
  export function useRef<T>(initialValue: T): { current: T };
  export function useRef<T>(initialValue: T | null): { current: T | null };
  export function useRef<T = undefined>(): { current: T | undefined };
  export function useContext<T>(context: any): T;
  export function useReducer<R extends any>(reducer: (state: any, action: any) => any, initialState: any, initializer?: (initialState: any) => any): [any, (action: any) => void];
  export function useLayoutEffect(effect: () => void | (() => void), deps?: any[]): void;
  export function useImperativeHandle<T>(ref: any, init: () => T, deps?: any[]): void;
  export function useDebugValue<T>(value: T, format?: (value: T) => any): void;
}

declare module 'react-dom' {
  export function render(element: any, container: any, callback?: () => void): any;
  export function hydrate(element: any, container: any, callback?: () => void): any;
  export function createPortal(children: any, container: any, key?: any): any;
  export function unmountComponentAtNode(container: any): boolean;
  export function findDOMNode(componentOrElement: any): any;
}

declare namespace JSX {
  interface Element extends React.ReactElement<any, any> { }
  interface ElementClass extends React.Component<any> {
    render(): React.ReactNode;
  }
  interface ElementAttributesProperty { props: {}; }
  interface ElementChildrenAttribute { children: {}; }
  interface IntrinsicAttributes extends React.Attributes { }
  interface IntrinsicClassAttributes<T> extends React.ClassAttributes<T> { }
  interface IntrinsicElements {
    [elemName: string]: any;
  }
}
