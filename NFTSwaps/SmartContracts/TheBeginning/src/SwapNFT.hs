{-# LANGUAGE DataKinds             #-}
{-# LANGUAGE DeriveAnyClass        #-}
{-# LANGUAGE DeriveGeneric         #-}
{-# LANGUAGE DerivingStrategies    #-}
{-# LANGUAGE FlexibleContexts      #-}
{-# LANGUAGE NoImplicitPrelude     #-}
{-# LANGUAGE NamedFieldPuns        #-}
{-# LANGUAGE OverloadedStrings     #-}
{-# LANGUAGE ScopedTypeVariables   #-}
{-# LANGUAGE TemplateHaskell       #-}
{-# LANGUAGE TypeApplications      #-}
{-# LANGUAGE TypeFamilies          #-}
{-# LANGUAGE TypeOperators         #-}
{-# LANGUAGE MultiParamTypeClasses #-}

module SwapNFT
  ( swapNFTScript
  , swapNFTScriptShortBs
  ) where

import           Codec.Serialise
import           Plutus.V1.Ledger.Contexts
import qualified PlutusTx
import           Cardano.Api.Shelley      (PlutusScript (..), PlutusScriptV1)
import           Prelude                  hiding (($))
import qualified Data.ByteString.Lazy     as LBS
import qualified Data.ByteString.Short    as SBS
import qualified Plutus.V1.Ledger.Scripts as Plutus
import qualified Ledger.Typed.Scripts     as Scripts
import           Ledger.Ada               as Ada
import           PlutusTx.Prelude         as P hiding (Semigroup (..), unless)
import           Ledger                   hiding (singleton)

data SwapParams = SwapParams
    { swapOwnerAddr :: !Address
    , swapLovelace  :: !Integer
    }
PlutusTx.makeLift ''SwapParams

{-# INLINABLE swapValidator #-}
swapValidator :: SwapParams -> BuiltinData -> BuiltinData -> ScriptContext -> Bool
swapValidator swap _ _ context
    | (contextCostCheck currentTxOutputs) = True
    | otherwise                           = traceIfFalse "Tx Error" $ False
    where
    
      info :: TxInfo
      info = scriptContextTxInfo context
      
      currentTxOutputs :: [TxOut]
      currentTxOutputs = txInfoOutputs info

      swapAmt :: Integer
      swapAmt = swapLovelace swap
      
      ownerAddr :: Address
      ownerAddr = swapOwnerAddr swap

      contextCostCheck :: [TxOut] -> Bool
      contextCostCheck [] = traceIfFalse "Swap ADA mismatch" $ False
      contextCostCheck (x:xs)
        | ((txOutAddress x) P.== ownerAddr) P.&& ((txOutValue x) P.== (Ada.lovelaceValueOf swapAmt)) = True
        | otherwise = contextCostCheck xs

data Typed
instance Scripts.ValidatorTypes Typed where
    type instance DatumType    Typed = BuiltinData
    type instance RedeemerType Typed = BuiltinData

typedValidator :: SwapParams -> Scripts.TypedValidator Typed
typedValidator swap = Scripts.mkTypedValidator @Typed
    ($$(PlutusTx.compile [|| swapValidator ||]) `PlutusTx.applyCode` PlutusTx.liftCode swap)
    $$(PlutusTx.compile  [|| wrap        ||])
  where
    wrap = Scripts.wrapValidator @BuiltinData @BuiltinData

validator :: Plutus.Validator
validator = Scripts.validatorScript (typedValidator swap)
    where swap = SwapParams { swapOwnerAddr = pubKeyHashAddress "ff413fb331a64930414bf07e7106a0488579d5329755d23c9ac0af49"
                            , swapLovelace = 105000000
                            }

script :: Plutus.Script
script = Plutus.unValidatorScript validator

swapNFTScriptShortBs :: SBS.ShortByteString
swapNFTScriptShortBs = SBS.toShort . LBS.toStrict $ serialise script

swapNFTScript :: PlutusScript PlutusScriptV1
swapNFTScript = PlutusScriptSerialised swapNFTScriptShortBs
