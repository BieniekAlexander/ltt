import React from 'react'
import { View, Text, StyleSheet, TextInput, Button } from 'react-native'
import { Formik } from 'formik'

const FormScreen = () => {
    return (
        <Formik
            initialValues={{ username: '', password: '' }}
        >
            {({ handleChange, handleSubmit, values }) => (
                <View>
                    <Text>Username</Text>
                    <TextInput
                        style={styles.input}
                        value={values.username}
                        onChangeText={handleChange('username')}
                    />
                    <Text>Password</Text>
                    <TextInput
                        style={styles.input}
                        value={values.password}
                        onChangeText={handleChange('password')}
                        secureTextEntry={true}
                    />
                    <Button onPress={handleSubmit} title="Submit" />
                </View>
            )}
        </Formik>
    )
}

const styles = StyleSheet.create({
    input: {
        margin: 15,
        borderColor: 'black',
        borderWidth: 1
    }
})

export default FormScreen