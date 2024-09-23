import React from 'react';
import {SafeAreaView, StyleSheet, View, Text, Button} from 'react-native';
import * as Network from "@userActions/Network";
import Onyx, {OnyxEntry, withOnyx} from "react-native-onyx";
import type {Network as NetworkOnyx, User as UserOnyx} from "@src/types/onyx";
import {withNetwork} from "./OnyxProvider";
import Switch from "./Switch";
import * as User from "@userActions/User";
import * as ApiUtils from "@libs/ApiUtils";
import compose from "@libs/compose";
import ONYXKEYS from "@src/ONYXKEYS";

type DebugOverlayWrapperPropsOnyxProps = {
    user: OnyxEntry<UserOnyx> | undefined;
};

type DebugOverlayWrapperProps = DebugOverlayWrapperPropsOnyxProps & {
    children: React.ReactNode;
    network: OnyxEntry<NetworkOnyx>;
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    overlayContainer: {
        position: 'absolute',
        bottom: 2,
        left: 24,
        transform: [{scale: 0.5}],
        transformOrigin: 'bottom left',
    },
    switchRow: {
        flexDirection: 'row',
        gap: 8,
    },
    tinySwitchContainer: {
        gap: 4,
        flexDirection: 'row',
        alignItems: 'center',
    },
    tinySwitchLabel: {
        fontSize: 24,
    },
});

type TinySwitchProps = {
    isOn: boolean;
    onToggle: () => void;
    accessibilityLabel: string,
    textLabel: string,
}

function TinySwitch({isOn, onToggle, accessibilityLabel, textLabel}: TinySwitchProps) {
    return (
        <View style={styles.tinySwitchContainer}>
            <Switch isOn={isOn} onToggle={onToggle} accessibilityLabel={accessibilityLabel}/>
            <Text style={styles.tinySwitchLabel}>{textLabel}</Text>
        </View>
    );
}

function DebugOverlayWrapper({children, user, network}: DebugOverlayWrapperProps) {
    const shouldUseStagingServer = user?.shouldUseStagingServer ?? ApiUtils.isUsingStagingApi();

    return (
        <View style={styles.container}>
            {children}
            <SafeAreaView style={styles.overlayContainer}>
                <View style={styles.switchRow}>
                    <TinySwitch
                        accessibilityLabel="Force offline"
                        isOn={!!network?.shouldForceOffline}
                        onToggle={() => Network.setShouldForceOffline(!network?.shouldForceOffline)}
                        textLabel="Offline"
                    />
                    <TinySwitch
                        accessibilityLabel="Use Staging Server"
                        isOn={shouldUseStagingServer}
                        onToggle={() => User.setShouldUseStagingServer(!shouldUseStagingServer)}
                        textLabel="Staging"
                    />
                    <Button
                        title="Reset"
                        onPress={() => {
                            // eslint-disable-next-line rulesdir/prefer-actions-set-data
                            Onyx.set(ONYXKEYS.RESET_REQUIRED, true).then((result) => {
                                // eslint-disable-next-line no-console
                                console.log("Reset successful");
                            }).catch((error) => {
                                console.error("Reset failed", error);
                            });
                        }}
                    />
                </View>
            </SafeAreaView>
        </View>
    )
}

export default compose(
    withOnyx<DebugOverlayWrapperProps, DebugOverlayWrapperPropsOnyxProps>({
        user: {
            key: ONYXKEYS.USER,
        },
    }),
    withNetwork(),
)(DebugOverlayWrapper);
