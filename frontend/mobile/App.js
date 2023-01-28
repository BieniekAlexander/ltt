/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React from 'react'
import { Node, useState, useEffect } from 'react'
import { Formik } from 'formik'
import axios from 'axios'
import * as Keychain from 'react-native-keychain'
import VocabularyBody from './src/components/VocabularyBody'
import FormComponent from './src/components/FormComponent'

import {
    SafeAreaView,
    ScrollView,
    StatusBar,
    StyleSheet,
    Text,
    TextInput,
    Button,
    useColorScheme,
    View,
} from 'react-native';

import {
    Colors
} from 'react-native/Libraries/NewAppScreen';

/* $FlowFixMe[missing-local-annot] The type annotation(s) required by Flow's
 * LTI update could not be added via codemod */
const Section = ({ children, title }) => {
    const isDarkMode = useColorScheme() === 'dark';
    return (
        <View style={styles.sectionContainer}>
            <Text
                style={[
                    styles.sectionTitle,
                    {
                        color: isDarkMode ? Colors.white : Colors.black,
                    },
                ]}>
                {title}
            </Text>
            <Text
                style={[
                    styles.sectionDescription,
                    {
                        color: isDarkMode ? Colors.light : Colors.dark,
                    },
                ]}>
                {children}
            </Text>
        </View>
    );
};


const App = () => {
    const isDarkMode = useColorScheme() === 'dark';
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userDetails, setUserDetails] = useState({});
    const [gotBackendResponse, setGotBackendResponse] = useState(false);

    useEffect(() => {
        (async () => {
            try {
                const credentials = await Keychain.getGenericPassword();
                if (credentials) {
                    setIsLoggedIn(true);
                    setUserDetails(credentials);
                }
            } catch (error) {
                console.log("Keychain couldn't be accessed!", error);
            }
        })();
    }, []);
    
    const handleLogin = async (username, password) => {
        /* store the credentials of the user in the user session */
        // ref: https://blog.logrocket.com/storing-credentials-using-react-native-keychain/
        await Keychain.setGenericPassword(username, password);
        setIsLoggedIn(true);
        setUserDetails({ username });

        // TODO add actual backend login call
    };

    const backgroundStyle = {
        backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
    };

    return (
        <SafeAreaView style={backgroundStyle}>
            <StatusBar
                barStyle={isDarkMode ? 'light-content' : 'dark-content'}
                backgroundColor={backgroundStyle.backgroundColor}
            />
            <ScrollView
                contentInsetAdjustmentBehavior="automatic"
                style={backgroundStyle}>
                <View
                    style={{
                        backgroundColor: isDarkMode ? Colors.black : Colors.white,
                    }}>
                    <Section title="Title">
                        {
                            isLoggedIn
                                ? `Welcome, ${userDetails.username}!`
                                : "Please Log in"
                        }

                    </Section>
                </View>
                {
                    gotBackendResponse
                    && <Section title="Hi please render"/>
                }
                {
                    isLoggedIn
                    ? <>
                        {/* <FormComponent/> */}
                        <VocabularyBody/>
                        <Button onPress={() => {setIsLoggedIn(false); setUserDetails({})}} title="Logout" />  
                    </>
                    : <>
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
                                    <Button onPress={() => handleLogin(values.username, values.password)} title="Submit" />
                                </View>
                            )}
                        </Formik>
                    </>
                }
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    sectionContainer: {
        marginTop: 32,
        paddingHorizontal: 24,
    },
    sectionTitle: {
        fontSize: 24,
        fontWeight: '600',
    },
    sectionDescription: {
        marginTop: 8,
        fontSize: 18,
        fontWeight: '400',
    },
    highlight: {
        fontWeight: '700',
    },
});

export default App;
