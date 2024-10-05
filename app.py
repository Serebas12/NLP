import streamlit as st

def main():
    st.title('TastyMap - Sabor en Palabras ')
    st.write("Este es un ejemplo simple de Streamlit.")
    if st.button('Decir hola'):
        st.write('Hola a todos!')
    nombre = st.text_input('¿Cuál es tu nombre?')
    if nombre:
        st.write(f'Hola, {nombre}!')

if __name__ == "__main__":
    main()


